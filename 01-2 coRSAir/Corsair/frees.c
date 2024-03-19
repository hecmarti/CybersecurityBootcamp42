#include	"coRSAir.h"
#include <openssl/x509.h>

int	free_ctx_ne(int n, BN_CTX	*ctx, mod_exp_t *n_e)
{
	if (n >= 0 && n < 6)
		BN_CTX_free(ctx);
	if (n >= 1 && n < 7)
		BN_free(n_e->n1);
	if (n >= 2)
		BN_free(n_e->n2);
	if (n >= 3 && n < 7)
		BN_free(n_e->e1);
	if (n >= 4)
		BN_free(n_e->e2);
	return (1);
}

int	free_get_n_e(BIO	*bioPub, X509 *cert, EVP_PKEY *pkey, RSA *rsa)
{
	if (bioPub != NULL)
		BIO_free(bioPub);
	if (cert != NULL)
		X509_free(cert);
	if (pkey != NULL)
		EVP_PKEY_free(pkey);
	if (rsa != NULL)
		RSA_free(rsa);
	return (1);
}

int	free_breaking(int nb, mod_exp_t *n_e, rsa_data_t *rsa_d, char *msg)
{
	if (nb == 3)
	{
  	BN_clear_free(rsa_d->p1);
  	BN_clear_free(rsa_d->q1);
  	BN_clear_free(rsa_d->dmp1);
  	BN_clear_free(rsa_d->dmq1);
  	BN_clear_free(rsa_d->iqmp);
  	BN_clear_free(rsa_d->phi);
	}
	if (nb == 2)
	{
		RSA_free(rsa_d->key);
  	BN_clear_free(rsa_d->phi);
  	BN_clear_free(rsa_d->p1);
  	BN_clear_free(rsa_d->q1);
	}
	if (nb == 3)
  	BN_clear_free(rsa_d->d);
	if (msg != NULL)
		free(msg);
	if (n_e != NULL)
	{
  	BN_clear_free(n_e->n2);
  	BN_clear_free(n_e->e2);
	}
	return (1);
}

int	free_rsa(int n, rsa_data_t *rsa_d)
{
	if (n == 0 || (n >= 2 && n < 11))
		BN_free(rsa_d->b);
	if (n == 1 || (n >= 2 && n < 11))
		BN_free(rsa_d->a);
	if (n >= 3 && n < 10)
		BN_free(rsa_d->d);
	if (n >= 4)
		BN_free(rsa_d->p1);
	if (n >= 5)
		BN_free(rsa_d->q1);
	if (n >= 6)
		BN_free(rsa_d->dmp1);
	if (n >= 7)
		BN_free(rsa_d->dmq1);
	if (n >= 8)
		BN_free(rsa_d->iqmp);
	if (n >= 9)
		BN_free(rsa_d->phi);
	if (n >= 10)
		RSA_free(rsa_d->key);
	return (1);
}
