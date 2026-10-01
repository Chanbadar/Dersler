#include<stdio.h>
#include<stdlib.h>

int main ()
{
	FILE *fp;
	if ((fp =fopen("eski_dosya.txt","w+"))==NULL)
	{
		printf("Dosya açılamadı");
		exit(1);
	}
	fputs("Bilgisayar",fp);
	fclose(fp);
	if(rename("eski_dosya.txt","yeni_dosya.txt")==0)
	{
		printf("Dosyanın adı başarıyla değiştirildi");
	}
	else{
		perror("Dosya adı değiştirilemedi");
	}
	return 0;
}

