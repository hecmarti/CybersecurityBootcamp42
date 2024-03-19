#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include	"coRSAir.h"


int	ft_check_ch(char *str)
{
	int	i;

	i = 0;
	if (!str)
		return (0);
	while (str[i])
	{
		if (str[i] == '\n' || str[i] == '\0')
			return (1);
		i++;
	}
	return (0);
}

char	*ft_last_check(char *line, char c)
{
	char	*str;
	int		i;

	i = 0;
	while (line[i])
		i++;
	str = (char *) malloc(2 + i);
	if (!str)
		return (NULL);
	i = 0;
	while (line[i])
	{
		str[i] = line[i];
		i++;
	}
	str[i] = c;
	str[i + 1] = '\0';
	free(line);
	return (str);
}

char	*get_next_line(int fd)
{
	char	*line;
	char	buff;
	int		reader;

	line = malloc(1);
	if (fd < 0 || !line)
		return (NULL);
	line[0] = '\0';
	reader = 1;
	while (!ft_check_ch(line) && reader != 0)
	{
		reader = read(fd, &buff, 1);
		if (reader <= 0)
		{
			if (line[0] == '\0' || reader < 0)
			{
				free(line);
				return (NULL);
			}
			return (line);
		}
		line = ft_last_check(line, buff);
	}
	return (line);
}
