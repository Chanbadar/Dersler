#include<stdio.h>
#include<stdlib.h>
#include<dirent.h>
#include<string.h>
#include<unistd.h>

#define BUFFER_SIZE 1024
void read_fdinfo(char *pid, char *fd)
{
 char fdinfo_path[BUFFER_SIZE];
 snprintf(fdinfo_path,BUFFER_SIZE,"/proc/%s/fdinfo/%s",pid,fd);
 FILE *fdinfo_file=fopen(fdinfo_path,"r");
 if (fdinfo_file==NULL){
     perror("fdinfo dosyası açılmadı");
     return;
}
char line[BUFFER_SIZE];
printf("FD %s için FDINFO:\n ",fd);
while (fgets(line,sizeof(line),fdinfo_file)!=NULL){
    printf("%s",line);

}
fclose(fdinfo_file);
printf("\n");

}
void list_fd(char *pid){
    char fd_dir[BUFFER_SIZE];
    snprintf(fd_dir,BUFFER_SIZE,"proc/%s/fd",pid);
    DIR *dir=opendir(fd_dir);
    if (dir==NULL){
        perror("fd dizini açılmadı");
        exit(EXIT_FAILURE);

    }
    struct dirent *entry;
    while ((entry=readdir(dir))!=NULL)
    {
        if (entry->d_name[0] != '.'){
            char fd_path[BUFFER_SIZE];
            snprintf(fd_path,BUFFER_SIZE,"/proc/%s/fd/%s",pid,entry->d_name);
            char link_target[BUFFER_SIZE];
            ssize_t len =readlink(fd_path,link_target,sizeof(link_target)-1);
            if(len!=-1){
                link_target[len]='\0';
                printf("FD %s->%s\n",entry->d_name,link_target);
                read_fdinfo(pid,entry->d_name);
            }
        }
    }
    closedir(dir);
}
int main ()
{
    pid_t pid=getpid();
    char pid_str[BUFFER_SIZE];
    snprintf(pid_str,BUFFER_SIZE,"%d",pid);
    printf("Process ID: %s\n", pid_str);
    printf("/proc/%s/fd dizinindeki dosya tanimlayicilar:\n",pid_str);
    list_fd(pid_str);
    return 0;
}
