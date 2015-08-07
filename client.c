/**************************************************************************
    
    (C) 2015 Aneesh Dogra
    (C) 2015 Kush \m/

**************************************************************************/

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT_TIME       13                  
#define PORT_FTP        21                  /* FTP connection port */
#define SERVER_ADDR     "192.168.1.133"     /* byld server */
#define MAXBUF          1024
#define DEBUG           1                   /* comment to swithc off interactive mode */
#define PORT            8888

int ** getgrid(char * str)
{
    int i, j;
    int ** grid = (int **) malloc(3 * sizeof(int *));

    for (i = 0; i < 3; i++)
        grid[i] = (int *) malloc(3 * sizeof(int));

    for (i = 0; i < 3; i++)
        for (j = 0; j < 3; j++)
            grid[i][j] = str[i * 3 + j] - '0';

    return grid;
}

void prettyprint(int ** grid)
{
    int i, j;

    for (i = 0; i < 3; i++)
    {
        for (j = 0; j < 3; j++)
            printf("%d ", grid[i][j]);

        printf("\n");
    }
}

int updategrid(int ** grid, int x, int y)
{
    if (x > 3 || y > 3 || x < 1 || y < 1)
        return 1;

    if (grid[x - 1][y - 1] != 0)
        return 2;
    else
        grid[x - 1][y - 1] = 1;
    
    return 0;    
}

char * gridtostring(int ** grid)
{   
    int i, j;

    char * str = (char *) malloc(11);

    for (i = 0; i < 3; i++)
        for (j = 0; j < 3; j++)
            str[i * 3 + j] = grid[i][j] + '0';

    str[10] = '\0';

    return str;

}










void analyze(int * x, int * y, int ** grid)
{
    // code your move, assign x and y to your move
}











int main()
{
    int sockfd;
    struct sockaddr_in dest;
    char *recv_buffer;
    char *send_buffer;
    int movex, movey;
    int ** grid;

    recv_buffer = (char *) malloc(20 * sizeof(char));
    send_buffer = (char *) malloc(20 * sizeof(char));

    /*---Open socket for streaming---*/
    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0 )
    {
        perror("Socket");
        exit(errno);
    }

    /*--- Initialize server address/port struct ---*/

    bzero(&dest, sizeof(dest));
    dest.sin_family = AF_INET;
    dest.sin_port = htons(PORT);

    if ( inet_aton(SERVER_ADDR, (struct in_addr *)&dest.sin_addr.s_addr) == 0 )
    {
        perror(SERVER_ADDR);
        exit(errno);
    }

    /*--- Connect to server ---*/

    if ( connect(sockfd, (struct sockaddr*)&dest, sizeof(dest)) != 0 )
    {
        perror("Connect ");
        exit(errno);
    }

    strcpy(send_buffer, "000000000");
    int n = write(sockfd, send_buffer, strlen(send_buffer));
    recv(sockfd, recv_buffer, 20, 0);

    while (strncmp(recv_buffer, "END", 3))
    {

        grid = getgrid(recv_buffer);
        prettyprint(grid);

        while (1)
        {

#ifdef DEBUG
            printf("Enter move (x y) [1 : 3] ");
            scanf("%d %d", &movex, &movey);

#else

            // CODE YOUR MOVE USING THIS FUNCTION

            analyze(&movex, &movey, grid); // your move
#endif

            if (updategrid(grid, movex, movey))
                printf("Invalid move\n");
            else
                break;
        }

        printf("");
        send_buffer = gridtostring(grid);
        send(sockfd, send_buffer, sizeof(send_buffer), 0);
        strcpy(recv_buffer, "000000000");

        recv(sockfd, recv_buffer, 20, 0);
    }

    printf("%s\n", recv_buffer);
    
    close(sockfd);
    return 0;
}


