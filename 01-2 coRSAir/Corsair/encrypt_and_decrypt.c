#include	"coRSAir.h"
#include <string.h>

static int	encrypt_err_handling(char **message, BIGNUM **bn_msg, int *len)
{
	*message = NULL;
	*message = get_next_line(0);
	if (*message == NULL && wr_err("Error\n", "can't read from stdin\n"))
		return (1);
	if (*message && (strlen(*message) > (size_t)*len)
			&& wr_err("Error\n", "Your message is too long\n"))
	{
		free(*message);
		return (1);
	}
	*bn_msg = NULL;
	*bn_msg = BN_new();
	if (*bn_msg == NULL && wr_err("Error\n", "Can't get your message\n"))
	{
		free(*message);
		return (1);
	}
	return (0);
}

static int	ascii_to_bin(char **message, BIGNUM **bn_msg)
{
	if (!BN_bin2bn((unsigned char *)*message, (int)strlen(*message) * sizeof(char), *bn_msg))
	{
		wr_err("Conversion Error\n", "can't pass ascii to bin\n");
		BN_free(*bn_msg);
		return (1);
	}
	printf("\n%sYour message is \n%s%s\n", RED_B_U, WHITE, *message);
	if (bn2dec_print("Your message passed to BN", *bn_msg))
	{
		wr_err("Print Error\n", "can't print message in bn\n");
		BN_free(*bn_msg);
		return (1);
	}
	return (0);
}

static BIGNUM	*ft_encrypt(BIGNUM **bn_msg, mod_exp_t *n_e, BN_CTX *ctx)
{
	BIGNUM	*encrypted;

	encrypted = NULL;
	encrypted = BN_new();
	if (!encrypted && wr_err("Cryto Error\n", "error when encrypting\n"))
	{
		BN_free(*bn_msg);
		return (NULL);
	}
	if (!BN_mod_exp(encrypted, *bn_msg, n_e->e1, n_e->n1, ctx)
			&& wr_err("Cryto Error\n", "can't calculate mod and exp\n"))
	{
		BN_free(*bn_msg);
		BN_free(encrypted);
		return (NULL);
	}
	if (bn2dec_print("\nencrypted", encrypted))
	{
		wr_err("Print Error\n", "can't print encrypted\n");
		BN_free(*bn_msg);
		BN_free(encrypted);
		return (NULL);
	}
	return (encrypted);
}

static BIGNUM	*ft_decrypt(BIGNUM *encrypted, mod_exp_t *n_e, rsa_data_t *rsa_d, BN_CTX *ctx)
{
	BIGNUM	*decrypted;

	decrypted = NULL;
	decrypted = BN_new();
	if (!decrypted && wr_err("Cryto Error\n", "error when decrypting\n"))
	{
		BN_free(encrypted);
		return (NULL);
	}
	if (!BN_mod_exp(decrypted, encrypted, rsa_d->d, n_e->n1, ctx))
	{
		wr_err("Cryto Error\n", "can't decrypt with mod and exp\n");
		BN_free(encrypted);
		BN_free(decrypted);
		return (NULL);
	}
	if (bn2dec_print("\ndecrypted", decrypted))
	{
		wr_err("Print Error\n", "can't print decrypted\n");
		BN_free(encrypted);
		BN_free(decrypted);
		return (NULL);
	}
	return (decrypted);
}

int	encrypting(mod_exp_t *n_e, rsa_data_t *rsa_d, BN_CTX *ctx, int len)
{
	char		*message;
	BIGNUM	*bn_msg;
	BIGNUM	*encrypted;
	BIGNUM	*decrypted;

	//Error Handling
	if (encrypt_err_handling(&message, &bn_msg, &len))
		return (free_breaking(2, n_e, rsa_d, NULL));

	//ASCII to BN
	if (ascii_to_bin(&message, &bn_msg))
		return (free_breaking(2, n_e, rsa_d, message));

	//Encrypting
	encrypted = ft_encrypt(&bn_msg, n_e, ctx);
	if (!encrypted)
		return (free_breaking(2, n_e, rsa_d, message));
	BN_free(bn_msg);

	//Decrypting
	decrypted = ft_decrypt(encrypted, n_e, rsa_d, ctx);
	if (!decrypted)
		return (free_breaking(2, n_e, rsa_d, message));
	BN_free(encrypted);

	//Printing Original Message
	char	origin_msg[64] = {};
	if (len > 64 || !BN_bn2bin(decrypted, (unsigned char *)origin_msg))
	{
		BN_free(decrypted);
		free_breaking(2, n_e, rsa_d, message);
		return (1);
	}
	printf("\n%sOriginal message is%s\n%s\n", RED_B_U, WHITE, origin_msg);
	BN_free(decrypted);
	free_breaking(2, n_e, rsa_d, message);
	BN_CTX_free(ctx);
	return (0);
}
