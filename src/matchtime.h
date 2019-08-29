#include <vector>
#include <string>
using namespace std;
class Matches {
	public:
		vector<int> gettimespan();
		Matches(vector<string> names, vector<int> timespan);
		vector<string> getnames();
		bool equals(vector<int> rhs);
		void addname(string name);

	private:
		vector<int> _timespan;
		vector<string> _filenames;
		
		//需要开始结束的时间，对应该时间下的所有文件的名称， 
};
