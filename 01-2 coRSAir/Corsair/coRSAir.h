#ifndef	CORSAIR_H
# define	CORSAIR_H

#include <openssl/rsa.h>

# define WHITE 			"\033[0m"				//Normal White
# define GREEN_B_U 	"\033[32;1;4m"	//Green Bold Underlined
# define RED 				"\033[91m"			//Red
# define RED_B_U 		"\033[91;1;4m"	//Red Bold Underlined
# define YEL_B_U 		"\033[93;1;4m"	//Yellow Bold Underlined
# define MAG_I 			"\033[95;3m"		//Magenta Italic

typedef struct rsa_data_s{
	BIGNUM		*a;
	BIGNUM		*b;
  BIGNUM		*d;
	BIGNUM		*p1;
  BIGNUM		*q1;
  BIGNUM		*dmp1;
  BIGNUM		*dmq1;
  BIGNUM		*iqmp;
  BIGNUM		*phi;
  RSA 			*key;
}rsa_data_t;

typedef struct mod_exp_s{
	BIGNUM		*n1;
	BIGNUM		*n2;
	BIGNUM		*e1;
	BIGNUM		*e2;
}mod_exp_t;

typedef struct file_info_s{
	BIO				*bioPub;
	X509			*cert;
	EVP_PKEY	*pkey;
	RSA				*rsa;
}file_info_t;

//main.c
int	bn2dec_print(char *name, BIGNUM *bn);

//gnl.c
char	*get_next_line(int fd);

//gnl_utils.c
char	*ft_strdup(char *s);
char	*ft_strjoin(char *s1, char const *s2);
char	*ft_strchr(char *s, int c);
char	*ft_substr(char *s, unsigned int start, size_t len);


//frees.c
int	free_ctx_ne(int n, BN_CTX	*ctx, mod_exp_t *n_e);
int	free_get_n_e(BIO	*bioPub, X509 *cert, EVP_PKEY *pkey, RSA *rsa);
int	free_breaking(int nb, mod_exp_t *n_e, rsa_data_t *rsa_d, char *msg);
int	free_rsa(int n, rsa_data_t *rsa_d);

//get_mod_exp.c
int	ft_get_module_exponent(char *file, BIGNUM	*n, BIGNUM *e);
int open__read_file(file_info_t *info, char *file);
int	get_pub_rsa(file_info_t *info);
int	get_mod_exp(file_info_t *info, BIGNUM *n, BIGNUM *e, const BIGNUM *tmp);

//error_handling.c
int	error_handling(int argc);
int	wr_err(char *str1, char *str2);
int	bn2dec_print(char *name, BIGNUM *bn);

//encrypt_and_decrypt.c
int	encrypting(mod_exp_t *n_e, rsa_data_t *rsa_d, BN_CTX *ctx, int len);

//creating_keys.c
int	create_private_key(rsa_data_t	*rsa_d, mod_exp_t	*n_e, BN_CTX	*ctx);

//rsa.c
int	init_rsa(rsa_data_t *rsa_d);
int	get_primes(rsa_data_t	*rsa_d, mod_exp_t	*n_e, BN_CTX	*ctx);
#endif
