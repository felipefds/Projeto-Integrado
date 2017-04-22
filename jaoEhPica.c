#include <stdio.h>
#include <string.h>

#define TEXTO_COMPLETO "90;135;90;45;"
#define MAX_CHARACTERES 3+1

int main (int argv, char *argc[])
{
	unsigned contadorTextoCompleto;
	unsigned contadorAngulo = 0;
	unsigned contadorStringAng = 0;
	char stringAngNorte[MAX_CHARACTERES];
	char stringAngLeste[MAX_CHARACTERES];
	char stringAngSul[MAX_CHARACTERES];
	char stringAngOeste[MAX_CHARACTERES];
	int intAngNorte;
	int intAngLeste;
	int intAngSul;
	int intAngOeste;
	char *validacao;
	
	for (contadorTextoCompleto = 0; contadorAngulo<4; contadorTextoCompleto++){
		
		if (TEXTO_COMPLETO[contadorTextoCompleto] != ';'){		
			if (contadorAngulo == 0)
				stringAngNorte[contadorStringAng] = TEXTO_COMPLETO[contadorTextoCompleto];
				
			if (contadorAngulo == 1)
				stringAngLeste[contadorStringAng] = TEXTO_COMPLETO[contadorTextoCompleto];
				
			if (contadorAngulo == 2)
				stringAngSul[contadorStringAng] = TEXTO_COMPLETO[contadorTextoCompleto];
				
			if (contadorAngulo == 3)
				stringAngOeste[contadorStringAng] = TEXTO_COMPLETO[contadorTextoCompleto];
			
			contadorStringAng++;
		}
	
		else{
			if (contadorAngulo == 0)
				stringAngNorte[contadorStringAng] = '\0';
				
			if (contadorAngulo == 1)
				stringAngLeste[contadorStringAng] = '\0';
					
			if (contadorAngulo == 2)
				stringAngSul[contadorStringAng] = '\0';
					
			if (contadorAngulo == 3)
				stringAngOeste[contadorStringAng] = '\0';
			
			contadorStringAng = 0;
			contadorAngulo++;
		}
		
	}
	
	printf ("%s\n", stringAngNorte);
	printf ("%s\n", stringAngLeste);
	printf ("%s\n", stringAngSul);
	printf ("%s\n", stringAngOeste);
	
	intAngNorte = strtoul(stringAngNorte, &validacao, 10);
	intAngLeste = strtoul(stringAngLeste, &validacao, 10);
	intAngSul = strtoul(stringAngSul, &validacao, 10);
	intAngOeste = strtoul(stringAngOeste, &validacao, 10);
	
	printf ("%i\n", intAngNorte+3);
	printf ("%i\n", intAngLeste+3);
	printf ("%i\n", intAngSul+3);
	printf ("%i\n", intAngOeste+3);

	return 0;
}
