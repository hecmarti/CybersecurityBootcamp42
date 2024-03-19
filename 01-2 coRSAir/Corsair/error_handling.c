#include	"coRSAir.h"
#include	<unistd.h>
#include <string.h>

int	error_handling(int argc)
{
	if (argc != 3)
	{
		wr_err("Wrong Arguments\n", "sytax:	./coRSAir cert1.pem cert2.pem\n");
		return (1);
	}
	return (0);
}

int	wr_err(char *str1, char *str2)
{
	write(2, "\n", 1);
	if (str1)
	{
		write(2, RED_B_U, strlen(RED_B_U));
		write(2, str1, strlen(str1));
		write(2, WHITE, strlen(WHITE));
	}
	if (str2)
	{
		write(2, RED, strlen(RED));
		write(2, str2, strlen(str2));
		write(2, WHITE, strlen(WHITE));
	}
	write(2, "\n", 1);
	return (1);
}

int	bn2dec_print(char *name, BIGNUM *bn)
{
	char	*value;

	value = NULL;
	value = BN_bn2dec(bn);
	if (value == NULL)
		return (1);
	printf("%s%s%s\n%s\n\n", MAG_I, name, WHITE, value);
	free(value);
	return (0);
}
