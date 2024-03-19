#include	"coRSAir.h"
#include <openssl/pem.h>

int create_pub_pkey(rsa_data_t *rsa_d, mod_exp_t *n_e)
{
	BIO		*pub_key;
	BIO		*priv_key;

	pub_key = NULL;
	priv_key = NULL;
	pub_key = BIO_new_file("my_pub_key.pem", "w");
	if (!pub_key && wr_err("Error\n", "can't create my_pub_key.pem\n"))
		return (free_breaking(2, n_e, rsa_d, NULL));
	priv_key = BIO_new_file("my_priv_key.pem", "w");
	if (!priv_key && wr_err("Error\n", "can't create my_priv_key.pem\n"))
	{
		BIO_free(pub_key);
		return (free_breaking(2, n_e, rsa_d, NULL));
	}
	if (!PEM_write_bio_RSAPublicKey(pub_key, rsa_d->key) && wr_err("Error\n", "can't write my_pub_key.pem\n"))
	{
		BIO_free(pub_key);
		BIO_free(priv_key);
		return (free_breaking(2, n_e, rsa_d, NULL));
	}
	if (!PEM_write_bio_RSAPrivateKey(priv_key, rsa_d->key, NULL, NULL, 0, NULL, NULL) && wr_err("Error\n", "can't write my_priv_key.pem\n"))
	{
		BIO_free(pub_key);
		BIO_free(priv_key);
		return (free_breaking(2, n_e, rsa_d, NULL));
	}
	BIO_free(pub_key);
	BIO_free(priv_key);
	return (0);
}

int set_new_key(rsa_data_t *rsa_d, mod_exp_t *n_e, BN_CTX *ctx)
{
  rsa_d->key = RSA_new();
  if (!rsa_d->key)
		return (free_rsa(9, rsa_d));
	if (!RSA_set0_key(rsa_d->key, n_e->n1, n_e->e1, rsa_d->d) 											//n, e and d
			&& wr_err("New Key Error\n", "n, e and d not set\n"))
	{
		free_ctx_ne(6, ctx, n_e);
		return (free_rsa(10, rsa_d));
	}
	if (!RSA_set0_factors(rsa_d->key, rsa_d->a, rsa_d->b)														//p and q
			&& wr_err("New Key Error\n", "p and q not set\n"))
	{
		free_ctx_ne(7, ctx, n_e);
		return (free_rsa(10, rsa_d));
	}
  if (!RSA_set0_crt_params(rsa_d->key, rsa_d->dmp1, rsa_d->dmq1, rsa_d->iqmp)			//dmp1, dmq1 and iqmp
			&& wr_err("New Key Error\n", "dmp1 and iqmp not set\n"))
	{
		free_ctx_ne(7, ctx, n_e);
		return (free_rsa(11, rsa_d));
	}
	if ((RSA_check_key(rsa_d->key) != 1)
			&& wr_err("New Key Error\n", "not a valid key generated\n"))
		return (free_breaking(2, n_e, rsa_d, NULL));
	return (0);
}

int calculate_rsa(rsa_data_t *rsa_d, mod_exp_t *n_e, BN_CTX *ctx)
{
  if (!BN_sub(rsa_d->p1, rsa_d->a, BN_value_one()) 						// p1 = p-1 
			&& wr_err("Math Error\n", "Can't calculate p1\n"))
		return (free_rsa(9, rsa_d));
  if (!BN_sub(rsa_d->q1, rsa_d->b, BN_value_one())						// q1 = q-1
			&& wr_err("Math Error\n", "Can't calculate q1\n"))
		return (free_rsa(9, rsa_d));
	if (!BN_mul(rsa_d->phi, rsa_d->p1, rsa_d->q1, ctx)					// phi(pq) = (p-1)*(q-1)
			&& wr_err("Math Error\n", "Can't calculate phi\n"))
		return (free_rsa(9, rsa_d));
  if (!BN_mod_inverse(rsa_d->d, n_e->e1, rsa_d->phi, ctx)			// d = e^-1 mod phi
			&& wr_err("Math Error\n", "Can't calculate d\n"))
		return (free_rsa(9, rsa_d));
  if (!BN_mod(rsa_d->dmp1, rsa_d->d, rsa_d->p1, ctx)					// dmp1 = d mod (p-1)
			&& wr_err("Math Error\n", "Can't calculate dmq1\n"))
		return (free_rsa(9, rsa_d));
  if (!BN_mod(rsa_d->dmq1, rsa_d->d, rsa_d->q1, ctx)					// dmq1 = d mod (q-1)
			&& wr_err("Math Error\n", "Can't calculate dmq1\n"))
		return (free_rsa(9, rsa_d));
  if (!BN_mod_inverse(rsa_d->iqmp, rsa_d->b, rsa_d->a, ctx)		// iqmp = q^-1 mod p
			&& wr_err("Math Error\n", "Can't calculate iqmp\n"))
		return (free_rsa(9, rsa_d));
	return (0);
}

int	calculate_rsa_param(rsa_data_t *rsa_d, mod_exp_t *n_e, BN_CTX *ctx)
{
	if (init_rsa(rsa_d))
		return	free_ctx_ne(6, ctx, n_e);
	if (calculate_rsa(rsa_d, n_e, ctx))
		return	free_ctx_ne(6, ctx, n_e);
	return (0);
}

int	create_private_key(rsa_data_t	*rsa_d, mod_exp_t	*n_e, BN_CTX	*ctx)
{
	//Calculating Private Key
	if (calculate_rsa_param(rsa_d, n_e, ctx))
		return (1);
	if (bn2dec_print("d", rsa_d->d) && wr_err("Error\n", "n1 not printed\n")
			&& free_ctx_ne(6, ctx, n_e))
		return (free_rsa(9, rsa_d));
	//Setting RSA to create Public and Private Keys
	if (set_new_key(rsa_d, n_e, ctx))
		return (1);
	//Creating Public and Private Keys .pem
	if (create_pub_pkey(rsa_d, n_e))
		return (1);
	return (0);
}
