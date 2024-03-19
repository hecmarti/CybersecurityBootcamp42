#include	"coRSAir.h"


int	get_primes(rsa_data_t	*rsa_d, mod_exp_t	*n_e, BN_CTX	*ctx)
{
	const BIGNUM	*one = BN_value_one();

	rsa_d->b = BN_new();
	if (!rsa_d->b && wr_err("Error\n", "q prime (b) not alloc\n"))
		return (1);
	rsa_d->a = BN_new();
	if (!rsa_d->a && wr_err("Error\n", "p prime (a) not alloc\n"))
		return (free_rsa(0, rsa_d));
	if (one == NULL && wr_err("Error\n", "one bn not created\n"))
		return (free_rsa(2, rsa_d));
	if (bn2dec_print("n1", n_e->n1) && wr_err("Error\n", "n1 not printed\n"))
		return (free_rsa(2, rsa_d));
	if (bn2dec_print("n2", n_e->n2) && wr_err("Error\n", "n2 not printed\n"))
		return (free_rsa(2, rsa_d));
	if (!BN_gcd(rsa_d->b, n_e->n1, n_e->n2, ctx) && wr_err("Error\n", "gcd not calculated\n"))
		return (free_rsa(2, rsa_d));
	if (!BN_cmp(rsa_d->b, one) && wr_err("Couldn't break RSA :(\n", "key's don't share primes\n"))
		return (free_rsa(2, rsa_d));
	if (bn2dec_print("q", rsa_d->b) && wr_err("Error\n", "q not printed\n"))
		return (free_rsa(2, rsa_d));
	if (!BN_div(rsa_d->a, NULL, n_e->n1, rsa_d->b, ctx) && wr_err("Error\n", "Impossible to calculate p\n"))
		return (free_rsa(2, rsa_d));
	if (bn2dec_print("p", rsa_d->a) && wr_err("Error\n", "p not printed\n"))
		return (free_rsa(2, rsa_d));
	return (0);
}

int	init_rsa(rsa_data_t *rsa_d)
{
  rsa_d->d = BN_new ();
	if (!rsa_d->d && wr_err("Error\n", "d not alloc\n"))
		return (free_rsa(2, rsa_d));
	rsa_d->p1 = BN_new ();
	if (!rsa_d->p1 && wr_err("Error\n", "p1 not alloc\n"))
		return (free_rsa(3, rsa_d));
  rsa_d->q1 = BN_new ();
	if (!rsa_d->q1 && wr_err("Error\n", "q1 not alloc\n"))
		return (free_rsa(4, rsa_d));
  rsa_d->dmp1 = BN_new ();
	if (!rsa_d->dmp1 && wr_err("Error\n", "dmp1 not alloc\n"))
		return (free_rsa(5, rsa_d));
  rsa_d->dmq1 = BN_new ();
	if (!rsa_d->dmq1 && wr_err("Error\n", "dmpq1 not alloc\n"))
		return (free_rsa(6, rsa_d));
  rsa_d->iqmp = BN_new ();
	if (!rsa_d->iqmp && wr_err("Error\n", "iqmp not alloc\n"))
		return (free_rsa(7, rsa_d));
  rsa_d->phi = BN_new ();
	if (!rsa_d->phi && wr_err("Error\n", "phi not alloc\n"))
		return (free_rsa(8, rsa_d));
	return (0);
}
