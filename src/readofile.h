#include <ostream>
#include <vector>
#include <string>
#include <fstream>
using namespace std;

class OFile {
public:
	OFile(string& filename);
	vector<int> gettimespan();
	string getfilename();
private:
	string _filename;
	vector<int> _timespan;
};