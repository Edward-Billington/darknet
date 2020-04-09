/* 
    Code was taken from 
    https://stackoverflow.com/questions/22077802/simple-c-example-of-doing-an-http-post-and-consuming-the-response/22135885
    by Jerry Jeremiah
    mofidied by Edward Billington

    Also
    https://github.com/jacketizer/libyuarel
    for the URL PARSE
*/
#include "custom_http.h"
#include <stdio.h> /* printf, sprintf */
#include <stdlib.h> /* exit, atoi, malloc, free */
#include <unistd.h> /* read, write, close */
#include <string.h> /* memcpy, memset */
#include <sys/socket.h> /* socket, connect */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */
#include <yuarel.h> // URL PARSER

int send_post_request(const char *url, const char *class, const float confidence)
{
    char *copy_url = malloc(strlen(url) + 1);
    strcpy(copy_url, url);

    // Using https://github.com/jacketizer/libyuarel. MIT License
    // struct yuarel url_obj;
    // url_obj.port = 3000;
    // url_obj.host = "127.0.0.1";
    // if (-1 == yuarel_parse(&url_obj, copy_url)) {
    //     fprintf(stderr, "Could not parse url!\n");
    //     return 1;
    // }

    int i;
    int portno = 3000;
    char *host = "127.0.0.1";
    struct hostent *server;
    struct sockaddr_in serv_addr;
    int sockfd, bytes, sent, received, total;

    // Create the message
    char message[4096];
    char data[1024];

    // Create JSON
    sprintf(data, "{\"object\":\"%s\", \"confidence\":\"%.0f\"}", class, confidence);
    // Create POST                    
    sprintf(message, "POST /%s HTTP/1.0\r\nContent-Type: application/json\r\nContent-Length: %d\r\n\r\n%s", "testing", strlen(data), data);

    /* create the socket */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) error("ERROR opening socket");

    /* lookup the ip address */
    server = gethostbyname(host);
    if (server == NULL) error("ERROR, no such host");

    /* fill in the structure */
    memset(&serv_addr,0,sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(portno);
    memcpy(&serv_addr.sin_addr.s_addr,server->h_addr,server->h_length);

    /* connect the socket */
    if (connect(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr)) < 0)
        error("ERROR connecting");

    /* send the request */
    total = strlen(message);
    sent = 0;
    do {
        bytes = write(sockfd,message+sent,total-sent);
        if (bytes < 0)
            error("ERROR writing message to socket");
        if (bytes == 0)
            break;
        sent+=bytes;
    } while (sent < total);

    /* receive the response */
    char response[4096];
    memset(response,0,sizeof(response));
    total = sizeof(response)-1;
    received = 0;
    do {
        bytes = read(sockfd,response+received,total-received);
        if (bytes < 0)
            error("ERROR reading response from socket");
        if (bytes == 0)
            break;
        received+=bytes;
    } while (received < total);

    if (received == total)
        error("ERROR storing complete response from socket");

    /* close the socket */
    close(sockfd);
    free(copy_url);

    /* process response */
    // printf("Response:\n%s\n",response);

    // Make sure the return was 200 OK
    char *check = strstr(response, "HTTP/1.1 200 OK");
    return check ? 1 : 0;
}