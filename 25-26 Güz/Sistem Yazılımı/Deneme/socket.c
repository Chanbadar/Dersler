#include<stdio.h>
#include<unistd.h>
#include<sys/socket.h>
#include<netinet/in.h>

int main (){
    int fd=socket(AF_INET,SOCK_STREAM,0);
    {
        if (fd==-1){
            perror("socket");
            return 1;

        }
        printf("Socket Başarıyla oluşturuldu FD numarasi:%d\n",fd);
        close (fd);
        printf("sokcet kapatildi");
        return 0;
    }
}
