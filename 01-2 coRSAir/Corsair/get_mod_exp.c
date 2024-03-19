#include	"coRSAir.h"
#include <openssl/x509.h>
#include <openssl/pem.h>

int	get_mod_exp(file_info_t *info, BIGNUM *n, BIGNUM *e, const BIGNUM *tmp)
{
	//Getting Exponent
	RSA_get0_key(info->rsa, NULL, &tmp, NULL);
	if (tmp == NULL && wr_err("Error\n", "Couldn't get exponent\n"))
		return (free_get_n_e(info->bioPub, info->cert, info->pkey, info->rsa));
	if (bn2dec_print("exponent", (BIGNUM *)tmp) && wr_err("Error\n", "exp not printed\n"))
		return (free_get_n_e(info->bioPub, info->cert, info->pkey, info->rsa));
	if (BN_copy(e, tmp) == NULL && wr_err("Error\n", "Exponent not alloc\n"))
		return (free_get_n_e(info->bioPub, info->cert, info->pkey, info->rsa));

	//Getting Module
	RSA_get0_key(info->rsa, &tmp, NULL,NULL);
	if (tmp == NULL && wr_err("Error\n", "Couldn't get module\n"))
		return (free_get_n_e(info->bioPub, info->cert, info->pkey, info->rsa));
	if (bn2dec_print("module", (BIGNUM *)tmp) && wr_err("Error\n", "mod not printed\n"))
		return (free_get_n_e(info->bioPub, info->cert, info->pkey, info->rsa));
	if (BN_copy(n, tmp) == NULL && wr_err("Error\n", "Module not alloc\n"))
		return (free_get_n_e(info->bioPub, info->cert, info->pkey, info->rsa));
	return (0);

}

int	get_pub_rsa(file_info_t *info)
{
	//Extracting Public Key
	info->pkey = X509_get_pubkey(info->cert);
	if (info->pkey == NULL && wr_err("Error\n", "Couldn't extract Public Key\n"))
		return free_get_n_e(info->bioPub, info->cert, NULL, NULL);

	//Extracting RSA
	info->rsa = EVP_PKEY_get1_RSA(info->pkey);
	if (info->rsa == NULL && wr_err("Error\n", "Couldn't get RSA data\n"))
		return free_get_n_e(info->bioPub, info->cert, info->pkey, NULL);
	return (0);
}

int open_read_file(file_info_t *info, char *file)
{

	//Basic Input Output
	info->bioPub = BIO_new_file(file, "r");
	if (info->bioPub == NULL && wr_err("Error\n", "Couldn't open that file\n"))
		return (1);

	//Read from x509 pem
	info->cert = PEM_read_bio_X509(info->bioPub, 0, 0, NULL);
	if (info->cert == NULL && wr_err("Error\n", "Couldn't read from file\n"))
		return free_get_n_e(info->bioPub, NULL, NULL, NULL);
	return (0);
}

int	ft_get_module_exponent(char *file, BIGNUM	*n, BIGNUM *e)
{
	file_info_t		info;
	const BIGNUM	*tmp;

	tmp = NULL;
	info = (file_info_t){.bioPub = NULL, .cert = NULL, .pkey = NULL, .rsa = NULL};
	printf("\n----------------  %s%s%s  ------------------\n", YEL_B_U, file, WHITE);
	if (open_read_file(&info, file))
		return (1);
	if (get_pub_rsa(&info))
		return (1);
	if (get_mod_exp(&info, n, e, tmp))
		return (1);
	RSA_free(info.rsa);
	EVP_PKEY_free(info.pkey);
	X509_free(info.cert);
	BIO_free(info.bioPub);
	printf("----------------------------------\n\n\n");
	return (0);
}
