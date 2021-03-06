#include "network.h"
#include "detection_layer.h"
#include "region_layer.h"
#include "cost_layer.h"
#include "utils.h"
#include "parser.h"
#include "box.h"
#include "image.h"
#include "demo.h"
#include <sys/time.h>
#include <yuarel.h> // URL PARSER

#define DEMO 1

#ifdef OPENCV

static char **demo_names;
static image **demo_alphabet;
static int demo_classes;

static network *net;
static image buff [3];
static image buff_letter[3];
static int buff_index = 0;
static void * cap;
static float fps = 0;
static float demo_thresh = 0;
static float demo_hier = .5;
static int running = 0;

static int demo_frame = 3;
static int demo_index = 0;
static float **predictions;
static float *avg;
static int demo_done = 0;
static int demo_total = 0;
static int detection_count = 0;
static int save_mode = 0;
static char *cpost_url = NULL;
static float total_fps = 0;
static float total_frames = 0;
static struct yuarel url_obj;
double demo_time;

detection *get_network_boxes(network *net, int w, int h, float thresh, float hier, int *map, int relative, int *num);

int size_network(network *net)
{
    int i;
    int count = 0;
    for(i = 0; i < net->n; ++i){
        layer l = net->layers[i];
        if(l.type == YOLO || l.type == REGION || l.type == DETECTION){
            count += l.outputs;
        }
    }
    return count;
}

void remember_network(network *net)
{
    int i;
    int count = 0;
    for(i = 0; i < net->n; ++i){
        layer l = net->layers[i];
        if(l.type == YOLO || l.type == REGION || l.type == DETECTION){
            memcpy(predictions[demo_index] + count, net->layers[i].output, sizeof(float) * l.outputs);
            count += l.outputs;
        }
    }
}

detection *avg_predictions(network *net, int *nboxes)
{
    int i, j;
    int count = 0;
    fill_cpu(demo_total, 0, avg, 1);
    for(j = 0; j < demo_frame; ++j){
        axpy_cpu(demo_total, 1./demo_frame, predictions[j], 1, avg, 1);
    }
    for(i = 0; i < net->n; ++i){
        layer l = net->layers[i];
        if(l.type == YOLO || l.type == REGION || l.type == DETECTION){
            memcpy(l.output, avg + count, sizeof(float) * l.outputs);
            count += l.outputs;
        }
    }
    detection *dets = get_network_boxes(net, buff[0].w, buff[0].h, demo_thresh, demo_hier, 0, 1, nboxes);
    return dets;
}

void *detect_in_thread(void *ptr)
{
    running = 1;
    float nms = .4;

    layer l = net->layers[net->n-1];
    float *X = buff_letter[(buff_index+2)%3].data;
    network_predict(net, X);
    remember_network(net);
    detection *dets = 0;
    int nboxes = 0;
    dets = avg_predictions(net, &nboxes);

    if (nms > 0) do_nms_obj(dets, nboxes, l.classes, nms);

    printf("\033[2J");
    printf("\033[1;1H");
    printf("\nFPS:%.1f\n",fps);
    printf("\nTOTAL FPS:%.1f\n",total_fps);
    printf("Objects:\n\n");
    if (fps < 144.0) {
        total_fps += fps;
        total_frames += 1;
    }
    image display = buff[(buff_index+2) % 3];
    draw_detections(display, dets, nboxes, demo_thresh, demo_names, demo_alphabet, demo_classes, &detection_count, save_mode, cpost_url, url_obj.port, url_obj.host, url_obj.path);
    free_detections(dets, nboxes);

    demo_index = (demo_index + 1)%demo_frame;
    running = 0;
    return 0;
}

void *fetch_in_thread(void *ptr)
{
    free_image(buff[buff_index]);
    buff[buff_index] = get_image_from_stream(cap);
    if(buff[buff_index].data == 0) {
        demo_done = 1;
        return 0;
    }
    letterbox_image_into(buff[buff_index], net->w, net->h, buff_letter[buff_index]);
    return 0;
}

void *display_in_thread(void *ptr)
{
    int c = show_image(buff[(buff_index + 1)%3], "Demo", 1);
    if (c != -1) c = c%256;
    if (c == 27) {
        demo_done = 1;
        return 0;
    } else if (c == 82) {
        demo_thresh += .02;
    } else if (c == 84) {
        demo_thresh -= .02;
        if(demo_thresh <= .02) demo_thresh = .02;
    } else if (c == 83) {
        demo_hier += .02;
    } else if (c == 81) {
        demo_hier -= .02;
        if(demo_hier <= .0) demo_hier = .0;
    }
    return 0;
}

void *display_loop(void *ptr)
{
    while(1){
        display_in_thread(0);
    }
}

void *detect_loop(void *ptr)
{
    while(1){
        detect_in_thread(0);
    }
}

void demo_save(char *cfgfile, char *weightfile, float thresh, int cam_index, const char *filename, char **names, int classes, int delay, char *prefix, int avg_frames, float hier, int w, int h, int frames, int fullscreen, char filenames[8][128], char *post_url)
{
    image **alphabet = load_alphabet();
    demo_names = names;
    demo_alphabet = alphabet;
    demo_classes = classes;
    demo_thresh = thresh;
    demo_hier = hier;
    printf("Demo\n");
    net = load_network(cfgfile, weightfile, 0);
    set_batch_network(net, 1);
    pthread_t detect_thread;
    pthread_t fetch_thread;
    save_mode = 1; // This is to enable saving the images - only in save mode.

    srand(2222222);
    int i;
    demo_total = size_network(net);
    predictions = calloc(demo_frame, sizeof(float*));
    for (i = 0; i < demo_frame; ++i){
        predictions[i] = calloc(demo_total, sizeof(float));
    }
    avg = calloc(demo_total, sizeof(float));

    // If there is a POST url
    if (post_url != NULL) {
        cpost_url = post_url;
        if (-1 == yuarel_parse(&url_obj, post_url)) {
            fprintf(stderr, "Could not parse url!\n");
            return;
        }
    }

    // Default case
    if (filenames == NULL) {
        if(filename && (strcmp(filename, "/") != 0)){
            printf("video file: %s\n", filename);
            cap = open_video_stream(filename, 0, 0, 0, 0);
        }else{
            cap = open_video_stream(0, cam_index, w, h, frames);
        }

        if(!cap) error("Couldn't connect to webcam.\n");

        buff[0] = get_image_from_stream(cap);
        buff[1] = copy_image(buff[0]);
        buff[2] = copy_image(buff[0]);
        buff_letter[0] = letterbox_image(buff[0], net->w, net->h);
        buff_letter[1] = letterbox_image(buff[0], net->w, net->h);
        buff_letter[2] = letterbox_image(buff[0], net->w, net->h);

        int count = 0;
        if(!prefix){
            make_window("Demo", 1352, 1013, fullscreen);
        }
      
        demo_time = what_time_is_it_now();
    
        while (!demo_done) {
            buff_index = (buff_index + 1) %3;
            if(pthread_create(&fetch_thread, 0, fetch_in_thread, 0)) error("Thread creation failed");
            if(pthread_create(&detect_thread, 0, detect_in_thread, 0)) error("Thread creation failed");
            if (!prefix) {
                fps = 1./(what_time_is_it_now() - demo_time);
                demo_time = what_time_is_it_now();
                display_in_thread(0);
            } else {
                char name[256];
                sprintf(name, "%s_%08d", prefix, count);
                save_image(buff[(buff_index + 1)%3], name);
            }
            pthread_join(fetch_thread, 0);
            pthread_join(detect_thread, 0);
            ++count;
        }
        printf("%d detections above the minimum confidence score of %.1f%%\n", detection_count, (thresh*100.0));
        printf("AVERAGE FPS: %.3f\n", total_fps/total_frames);
    } else { // Case for the -folder flag, iterate over each
        for(int i = 0; i < sizeof(filenames); i++) {
            demo_done = 0;
            buff_index = 0;
            total_fps = 0;
            total_frames = 0;
            char *current_file = filenames[i];
            
            if (strcmp(current_file, "")) {
                cap = open_video_stream(current_file, 0, 0, 0, 0);
            
                buff[0] = get_image_from_stream(cap);
                buff[1] = copy_image(buff[0]);
                buff[2] = copy_image(buff[0]);
                buff_letter[0] = letterbox_image(buff[0], net->w, net->h);
                buff_letter[1] = letterbox_image(buff[0], net->w, net->h);
                buff_letter[2] = letterbox_image(buff[0], net->w, net->h);
            
                int count = 0;
                demo_time = what_time_is_it_now();
            
                while (!demo_done) {
                    buff_index = (buff_index + 1) %3;
                    if(pthread_create(&fetch_thread, 0, fetch_in_thread, 0)) error("Thread creation failed");
                    if(pthread_create(&detect_thread, 0, detect_in_thread, 0)) error("Thread creation failed");
                    if (!prefix) {
                        fps = 1./(what_time_is_it_now() - demo_time);
                        demo_time = what_time_is_it_now();
                        display_in_thread(0);
                    } else {
                        char name[256];
                        sprintf(name, "%s_%08d", prefix, count);
                        save_image(buff[(buff_index + 1)%3], name);
                    }
                    pthread_join(fetch_thread, 0);
                    pthread_join(detect_thread, 0);
                    ++count;
                }
            }
        }

        printf("%d detections above the minimum confidence score of %.1f%%\n", detection_count, (thresh*100.0));
    }
}

void demo(char *cfgfile, char *weightfile, float thresh, int cam_index, const char *filename, char **names, int classes, int delay, char *prefix, int avg_frames, float hier, int w, int h, int frames, int fullscreen)
{
    //demo_frame = avg_frames;
    image **alphabet = load_alphabet();
    demo_names = names;
    demo_alphabet = alphabet;
    demo_classes = classes;
    demo_thresh = thresh;
    demo_hier = hier;
    printf("Demo\n");
    net = load_network(cfgfile, weightfile, 0);
    set_batch_network(net, 1);
    pthread_t detect_thread;
    pthread_t fetch_thread;

    srand(2222222);

    int i;
    demo_total = size_network(net);
    predictions = calloc(demo_frame, sizeof(float*));
    for (i = 0; i < demo_frame; ++i){
        predictions[i] = calloc(demo_total, sizeof(float));
    }
    avg = calloc(demo_total, sizeof(float));

    if(filename){
        printf("video file: %s\n", filename);
        cap = open_video_stream(filename, 0, 0, 0, 0);
    }else{
        cap = open_video_stream(0, cam_index, w, h, frames);
    }

    if(!cap) error("Couldn't connect to webcam.\n");

    buff[0] = get_image_from_stream(cap);
    buff[1] = copy_image(buff[0]);
    buff[2] = copy_image(buff[0]);
    buff_letter[0] = letterbox_image(buff[0], net->w, net->h);
    buff_letter[1] = letterbox_image(buff[0], net->w, net->h);
    buff_letter[2] = letterbox_image(buff[0], net->w, net->h);

    int count = 0;
    if(!prefix){
        make_window("Demo", 1352, 1013, fullscreen);
    }

    demo_time = what_time_is_it_now();

    while(!demo_done){
        buff_index = (buff_index + 1) %3;
        if(pthread_create(&fetch_thread, 0, fetch_in_thread, 0)) error("Thread creation failed");
        if(pthread_create(&detect_thread, 0, detect_in_thread, 0)) error("Thread creation failed");
        if(!prefix){
            fps = 1./(what_time_is_it_now() - demo_time);
            demo_time = what_time_is_it_now();
            display_in_thread(0);
        }else{
            char name[256];
            sprintf(name, "%s_%08d", prefix, count);
            save_image(buff[(buff_index + 1)%3], name);
        }
        pthread_join(fetch_thread, 0);
        pthread_join(detect_thread, 0);
        ++count;
    }
}
#else
void demo(char *cfgfile, char *weightfile, float thresh, int cam_index, const char *filename, char **names, int classes, int delay, char *prefix, int avg, float hier, int w, int h, int frames, int fullscreen)
{
    fprintf(stderr, "Demo needs OpenCV for webcam images.\n");
}
#endif

