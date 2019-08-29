#include"matchtime.h"


Matches::Matches(vector<string> names, vector<int> timespan): _filenames(names), _timespan(timespan)
{
}

vector<string> Matches::getnames(){
	return _filenames;
}

bool Matches::equals(vector<int> rhs)
{
	if (this->gettimespan == rhs) {
		return true;
	}
	else {
		return false;
	}
}

void Matches::addname(string name)
{
	this->_filenames.push_back(name);
}

vector<int> Matches::gettimespan() {
	return _timespan;
}