#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <iomanip>
using namespace std;

int main(){
int error = 0;
std::stringstream cmd;
cmd << "/home/sedm/Queue/sedmv2/" << "get_observation";
error = system(cmd.str().c_str());
cout << "error code " << error;
if(WEXITSTATUS(error) == 0){
	cout << "here";
};
// return 0;
}
// printf(WEXITSTATUS(error));
