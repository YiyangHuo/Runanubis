#include "tinyxml.h"
#include "fileelement.h"


class TheFile {
public:
	TheFile(string& filename);
	vector <Fileelement>getInfo();
private:
	vector<Fileelement> _timeinfo;
};