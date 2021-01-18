#include <iostream>
#include <list>
#include <map>
#include <queue>
#include <chrono> 

using namespace std;
using namespace std::chrono; 

class Navigation
{
    map<pair<int, int>, list<pair<int, int>>> graph;
    pair<int, int> pos;
    pair<int, int> goal;
    list<pair<int, int>> path;

public:
    Navigation();

    bool setPosition(int x, int y);

    bool setGoal(int x, int y);

    void addPath(pair<int, int> v, pair<int, int> w);

    void removePath(pair<int, int> v, pair<int, int> w);

    void removeNode(pair<int, int> v);

    bool calculatePath();

    pair<pair<int, int>, pair<int, int>> navigate();
};

Navigation::Navigation()
{
    this->graph = map<pair<int, int>, list<pair<int, int>>>();
    this->pos = pair<int, int>();
    this->goal = pair<int, int>();
    this->path = list<pair<int, int>>();
}

bool Navigation::setPosition(int x, int y)
{
    if (this->graph.find(pair<int, int>(x, y)) == this->graph.end())
        return false;
    this->pos.first = x;
    this->pos.second = y;
    return true;
}

bool Navigation::setGoal(int x, int y)
{
    this->goal.first = x;
    this->goal.second = y;
    return true;
}

void Navigation::addPath(pair<int, int> v, pair<int, int> w)
{
    if (this->graph.find(v) == this->graph.end())
    {
        this->graph.insert(pair<pair<int, int>, list<pair<int, int>>>(v, list<pair<int, int>>()));
        this->graph.at(v).push_back(w);
    }
    else
    {
        this->graph.at(v).push_back(w);
    }
}

void Navigation::removePath(pair<int, int> v, pair<int, int> w)
{
    this->graph.at(v).remove(w);
}

void Navigation::removeNode(pair<int, int> v)
{
    this->graph.erase(v);
    map<pair<int, int>, list<pair<int, int>>>::iterator itr;
    for (itr = this->graph.begin(); itr != this->graph.end(); ++itr)
    {
        this->graph.at(itr->first).remove(v);
    }
}

bool Navigation::calculatePath()
{
    map<pair<int, int>, pair<int, int>> path;
    queue<pair<int, int>> queue;
    queue.push(this->pos);

    while (!queue.empty())
    {
        pair<int, int> node = queue.front();
        queue.pop();
        for (pair<int, int> p : this->graph.at(node))
        {

            if (path.find(p) == path.end())
            {
                path.insert(pair<pair<int, int>, pair<int, int>>(p, node));
                queue.push(p);
                if (p == this->goal)
                {
                    this->path.clear();
                    pair<int, int> temp;
                    temp = p;
                    this->path.push_front(temp);
                    while (path.at(temp) != this->pos)
                    {
                        temp = path.at(temp);
                        this->path.push_front(temp);
                    }
                    return true;
                }
            }
        }
    }
    this->path.clear();
    return false;
}

pair<pair<int, int>, pair<int, int>> Navigation::navigate()
{
    pair<int, int> past_pos = this->pos;
    this->pos = this->path.front();
    this->path.pop_front();
    return make_pair(past_pos, this->pos);
}

void createDummy(Navigation &x, int n)
{
    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            if (i > 0 && j > 0 && i < n - 1 && j < n - 1)
            {
                x.addPath(make_pair(i, j), make_pair(i - 1, j));
                x.addPath(make_pair(i, j), make_pair(i + 1, j));
                x.addPath(make_pair(i, j), make_pair(i, j - 1));
                x.addPath(make_pair(i, j), make_pair(i, j + 1));
            }
            else if (i == 0 && j == 0 && n > 1)
            {
                x.addPath(make_pair(0, 0), make_pair(0, 1));
                x.addPath(make_pair(0, 0), make_pair(1, 0));
            }
            else if (i == 0 && j == n - 1 && n > 1)
            {
                x.addPath(make_pair(i, j), make_pair(i + 1, j));
                x.addPath(make_pair(i, j), make_pair(i, j - 1));
            }
            else if (i == n - 1 && j == 0 && n > 1)
            {
                x.addPath(make_pair(i, j), make_pair(i - 1, j));
                x.addPath(make_pair(i, j), make_pair(i, j + 1));
            }
            else if (i == n - 1 && j == n - 1 && n > 1)
            {
                x.addPath(make_pair(i, j), make_pair(i - 1, j));
                x.addPath(make_pair(i, j), make_pair(i, j - 1));
            }
            else if (i == 0 && j != n - 1 && j != 0 && n > 1)
            {
                x.addPath(make_pair(i, j), make_pair(i + 1, j));
                x.addPath(make_pair(i, j), make_pair(i, j - 1));
                x.addPath(make_pair(i, j), make_pair(i, j + 1));
            }
            else if (j == 0 && i != n - 1 && i != 0 && n > 1)
            {
                x.addPath(make_pair(i, j), make_pair(i - 1, j));
                x.addPath(make_pair(i, j), make_pair(i + 1, j));
                x.addPath(make_pair(i, j), make_pair(i, j + 1));
            }
            else if (i == n - 1 && j != n - 1 && j != 0 && n > 1)
            {
                x.addPath(make_pair(i, j), make_pair(i - 1, j));
                x.addPath(make_pair(i, j), make_pair(i, j - 1));
                x.addPath(make_pair(i, j), make_pair(i, j + 1));
            }
            else if (j == n - 1 && i != n - 1 && i != 0 && n > 1)
            {
                x.addPath(make_pair(i, j), make_pair(i - 1, j));
                x.addPath(make_pair(i, j), make_pair(i + 1, j));
                x.addPath(make_pair(i, j), make_pair(i, j - 1));
            }
        }
    }
}

int main()
{
    Navigation navigation = Navigation();
    createDummy(navigation, 1000);
    // navigation.addPath(make_pair(0, 0), make_pair(0, 1));
    // navigation.addPath(make_pair(0, 1), make_pair(1, 0));
    // navigation.addPath(make_pair(1, 0), make_pair(1, 1));
    // navigation.addPath(make_pair(1, 1), make_pair(1, 2));
    // navigation.addPath(make_pair(1, 2), make_pair(1, 3));
    // navigation.addPath(make_pair(1, 2), make_pair(1, 4));
    navigation.setPosition(0, 0);
    navigation.setGoal(999, 999);
    cout << "created" << endl;
    auto start = high_resolution_clock::now(); 
    navigation.calculatePath();
    auto stop = high_resolution_clock::now(); 
    auto duration = duration_cast<microseconds>(stop - start); 
    cout << "Time taken by function: "
         << duration.count() << " microseconds" << endl; 
    return 0;
}
