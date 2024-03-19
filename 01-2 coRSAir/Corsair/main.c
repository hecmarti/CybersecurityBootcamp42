#include <openssl/evp.h>
#include <openssl/ssl.h>
#include <openssl/rsa.h>
#include <openssl/x509.h>
#include <openssl/pem.h>

#include <string.h>
#include	<unistd.h>

#include	"coRSAir.h"

int	ft_break_rsa(mod_exp_t	*n_e, BN_CTX *ctx)
{
	int	bits;
	rsa_data_t	rsa_d;

	bits = 0;
	rsa_d = (rsa_data_t){.a = NULL, .b = NULL, .d = NULL, .p1 = NULL, .q1 = NULL,
		.dmp1 = NULL, .dmq1 = NULL, .iqmp = NULL, .phi = NULL, .key = NULL};
	printf("----------------  %sBreaking RSA%s  ------------------\n", GREEN_B_U, WHITE);
	if (get_primes(&rsa_d, n_e, ctx))
		return	free_ctx_ne(6, ctx, n_e);
	printf("----------------------------------\n\n\n");

	printf("----------------  %sGenerating Private Key%s  ------------------\n", GREEN_B_U, WHITE);
	if (create_private_key(&rsa_d, n_e, ctx))
		return (1);
	printf("----------------------------------\n\n\n");

	printf("----------------  %sEncrypting Message%s  ------------------\n", GREEN_B_U, WHITE);
	bits = BN_num_bits(n_e->n1);
	if (bits != 512 && wr_err("Size error\n", "RSA size must be 512\n"))
		return (free_breaking(2, n_e, &rsa_d, NULL));
	printf("Insert here your text (%d bits max.) to be encrypted:\n", bits);
//Estoy aquí
	if (encrypting(n_e, &rsa_d, ctx, bits / 8))
		return (1);
	printf("----------------------------------\n\n\n");
	return (0);
}

int	init_ctx_and_ne(BN_CTX	*ctx, mod_exp_t	*n_e)
{
	//Init ctx
	if (ctx == NULL && wr_err("Error\n", "ctx not initialized\n"))
		return	free_ctx_ne(0, ctx, n_e);

	//Init n and e
	n_e->n1 = BN_new ();
	if (n_e->n1 == NULL && wr_err("Error\n", "n1 not initialized\n"))
		return	free_ctx_ne(1, ctx, n_e);
	n_e->n2 = BN_new ();
	if (n_e->n2 == NULL && wr_err("Error\n", "n2 not initialized\n"))
		return	free_ctx_ne(2, ctx, n_e);
	n_e->e1 = BN_new ();
	if (n_e->e1 == NULL && wr_err("Error\n", "e1 not initialized\n"))
		return	free_ctx_ne(3, ctx, n_e);
	n_e->e2 = BN_new ();
	if (n_e->e2 == NULL && wr_err("Error\n", "e2 not initialized\n"))
		return	free_ctx_ne(4, ctx, n_e);
	return (0);
}

int	main(int argc, char **argv)
{
	mod_exp_t	n_e;

	n_e = (mod_exp_t){.n1 = NULL, .n2 = NULL, .e1 = NULL, .e2 = NULL};

	//Error Handling
	if (error_handling(argc))
		return (1);

	//Configure CTX
	BN_CTX	*ctx = NULL;
	ctx = BN_CTX_new();
	if (init_ctx_and_ne(ctx, &n_e))
		return	(1);

	//Getting module and exponent
	if (ft_get_module_exponent(argv[1], n_e.n1, n_e.e1))
		return	(free_ctx_ne(5, ctx, &n_e));
	if (ft_get_module_exponent(argv[2], n_e.n2, n_e.e2))
		return	(free_ctx_ne(5, ctx, &n_e));


// TO DO COMPROBADO Y PERFECTO HASTA AQUÍ

	//Breaking RSA
	if (ft_break_rsa(&n_e, ctx))
	{
		BN_CTX_free(ctx);
		return	(1);
	}

	return 0;
}
