#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    for(int i=0 ;i < 128; i++)
    {
        int x = (i%4) + ((i/16)*4);
        int y = (i- ((i/4)%4))%4;

        cout << i << " :  " << (32*y + x)<< endl;
    }
    return 0;
}