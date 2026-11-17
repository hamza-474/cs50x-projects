#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool valid_key(string key);

int main(int argc, string argv[])
{
    if (argc != 2 || !valid_key(argv[1]))
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];
    string plaintext = get_string("plaintext:  ");

    printf("ciphertext: ");
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isupper(plaintext[i]))
        {
            printf("%c", toupper(key[plaintext[i] - 65]));
        }
        else if (islower(plaintext[i]))
        {
            printf("%c", tolower(key[plaintext[i] - 97]));
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
    return 0;
}

bool valid_key(string key)
{
    if (strlen(key) != 26)
    {
        return false;
    }
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }
    }

    bool seen[26] = {false};
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        int index = toupper(key[i]) - 65;
        if (seen[index])
        {
            return false;
        }
        seen[index] = true;
    }

    return true;
}
