#include <stdio.h>
#include <stdlib.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>

#include <stdio.h>
#include <stdlib.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    int fd;
    // Name of the port we will be using, Rasberry Pi model B (i2c-1)
    char *fileName = "/dev/i2c-1";
    int  address = 0x27;// Address of I2C device
    char buf[100];

    if ((fd = open (fileName, O_RDWR)) < 0) {// Open port for reading and writing
        printf("Failed to open i2c port\n");
        exit(1);
    }
    // Set the port options and set the address of the device
    if (ioctl(fd, I2C_SLAVE, address) < 0) {
        printf("Unable to get bus access to talk to slave\n");
        exit(1);
    }
    if (argc>1)
    {
        sprintf(buf,argv[1]);
        //printf("%s %d %s\n",buf,strlen(buf),buf[strlen(buf)]);
        if ((write(fd, buf, strlen(buf)+1)) != strlen(buf)+1) {
            printf("Error writing to i2c slave\n");
            exit(1);
        }
    } else {
        printf(" Simple tool to send commands to Digole graphic adapter\nexamples:\n");
        printf(" rpi_lcd \"CLTTHello Word\" - Clear the screen (CL) and prints \"Hello Word\" (TT)\n");
        printf(" rpi_lcd \"CC002\" - Draws a cirle at x=30 (0), y=30 (0) with a radio of 32 (2)\n");    //not for Character LCD
    }
    return 0;
}
