// Recovers JPEGs from a forensic image of a memory card

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open memory card
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Buffer for a block of data
    uint8_t buffer[512];

    // Count of JPEGs found
    int count = 0;

    // Current output file
    FILE *output = NULL;

    // File name for the current JPEG
    char filename[8];

    // Read blocks until the end of the card
    while (fread(buffer, sizeof(uint8_t), 512, input) == 512)
    {
        // Check for the start of a JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // Close the previous JPEG, if one is open
            if (output != NULL)
            {
                fclose(output);
            }

            // Open a new JPEG file
            sprintf(filename, "%03i.jpg", count);
            count++;
            output = fopen(filename, "w");
            if (output == NULL)
            {
                fclose(input);
                printf("Could not create file.\n");
                return 1;
            }
        }

        // Write the block to the current JPEG, if one is open
        if (output != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), 512, output);
        }
    }

    // Close files
    if (output != NULL)
    {
        fclose(output);
    }
    fclose(input);
    return 0;
}
