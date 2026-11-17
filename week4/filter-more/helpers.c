// Helper functions for filter

#include "helpers.h"

#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = (int) round(
                (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumBlue = 0;
            int sumGreen = 0;
            int sumRed = 0;
            int count = 0;
            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    int row = i + k;
                    int col = j + l;
                    if (row >= 0 && row < height && col >= 0 && col < width)
                    {
                        sumBlue += copy[row][col].rgbtBlue;
                        sumGreen += copy[row][col].rgbtGreen;
                        sumRed += copy[row][col].rgbtRed;
                        count++;
                    }
                }
            }
            image[i][j].rgbtBlue = (int) round((float) sumBlue / count);
            image[i][j].rgbtGreen = (int) round((float) sumGreen / count);
            image[i][j].rgbtRed = (int) round((float) sumRed / count);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gxBlue = 0;
            int gxGreen = 0;
            int gxRed = 0;
            int gyBlue = 0;
            int gyGreen = 0;
            int gyRed = 0;
            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    int row = i + k;
                    int col = j + l;
                    if (row >= 0 && row < height && col >= 0 && col < width)
                    {
                        gxBlue += copy[row][col].rgbtBlue * gx[k + 1][l + 1];
                        gxGreen += copy[row][col].rgbtGreen * gx[k + 1][l + 1];
                        gxRed += copy[row][col].rgbtRed * gx[k + 1][l + 1];
                        gyBlue += copy[row][col].rgbtBlue * gy[k + 1][l + 1];
                        gyGreen += copy[row][col].rgbtGreen * gy[k + 1][l + 1];
                        gyRed += copy[row][col].rgbtRed * gy[k + 1][l + 1];
                    }
                }
            }
            int blue = (int) round(sqrt(gxBlue * gxBlue + gyBlue * gyBlue));
            int green = (int) round(sqrt(gxGreen * gxGreen + gyGreen * gyGreen));
            int red = (int) round(sqrt(gxRed * gxRed + gyRed * gyRed));
            image[i][j].rgbtBlue = blue > 255 ? 255 : blue;
            image[i][j].rgbtGreen = green > 255 ? 255 : green;
            image[i][j].rgbtRed = red > 255 ? 255 : red;
        }
    }
    return;
}
