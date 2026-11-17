#include <cs50.h>
#include <stdbool.h>
#include <stdio.h>

int main(void)
{
    long number = get_long("Number: ");
    long temp = number;
    int digits = 0;
    int sum = 0;
    bool alternate = false;
    while (temp > 0)
    {
        int digit = temp % 10;
        if (alternate)
        {
            int doubled = digit * 2;
            sum += doubled / 10 + doubled % 10;
        }
        else
        {
            sum += digit;
        }
        alternate = !alternate;
        temp /= 10;
        digits++;
    }
    long start = number;
    while (start >= 100)
    {
        start /= 10;
    }
    if (sum % 10 != 0)
    {
        printf("INVALID\n");
    }
    else if (digits == 15 && (start == 34 || start == 37))
    {
        printf("AMEX\n");
    }
    else if (digits == 16 && start >= 51 && start <= 55)
    {
        printf("MASTERCARD\n");
    }
    else if ((digits == 13 || digits == 16) && start / 10 == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
