#include <stdio.h>
#include <stdlib.h>
int main ()
{
FILE *fp;
if((fp=fopen("ornek.txt","w+"))== NULL)
{
	printf("Dosya açılmadı");
	exit(1);
}
fputs("Bilgisayar",fp);
fclose(fp);
if (remove ("ornek.txt")==0)
{
printf("Dosya başarıyla silindi");

}
else {perror("Dosya silinemedi");
}
return 0;
}

