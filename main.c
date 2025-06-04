#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
 FILE *arquivo; //declara ponteiro para arquivo
 char palavra[100];
 printf("Escreva o nome do arquivo que contém os comandos Assembly: ");
 scanf("%99s", palavra);
 printf("%d ",palavra);
//  arquivo = fopen("dados.txt", "r"); //abre arquivo
//  if (arq != NULL){ // checa se não deu erro na abertura do arquivo
//  … //processa arquivo
//  fclose(arq); //fecha arquivo
//  } else printf("Erro ao abrir arquivo\n");
}