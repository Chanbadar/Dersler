#include<stdio.h>
#include<unistd.h>
#include<sys/wait.h>
int main ()
{
    pid_t pid= fork();
    if(pid==0)
    {
        printf("Child process çalışıyor, PID= %d\n",getpid());
        execlp("/bin/ls","ls",NULL);
    }
	else if (pid>0)
	{
		printf("Parent prcess çalışıyor,PID=%d\n",getpid());
		wait(NULL);
	}
	else
	{
		printf("Fork Başarısız oldu!\n");
	}
return 0;
} 
