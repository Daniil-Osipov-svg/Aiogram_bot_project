#include <iostream>
#include <stdlib.h>
#include <cstdlib>
#include <ctime>
#include <stdio.h>
#include <iomanip>

#include <initializer_list>

using namespace std;

class massive{
	private:
		int* data = NULL;
		int size = 0;

	public:

		massive(){
			size = 5;
			data = new int[size]{1, 2, 3, 4, 5};
		}

		massive(initializer_list<int> list)
		{
			data = new int [list.size()];
			size = list.size();
			int i = 0;
	        for (int val : list) {
	            data[i++] = val;
	        }
		}

		massive(const massive& other){
			data = new int [other.size];
			size = other.size;

			for (int i = 0; i < size; ++i) {
	            data[i] = other.data[i];
	        }
		}

		float srednee(){

		    float summ = 0;
		    for (int i = 0; i < size; ++i){
				summ = summ + data[i];
			}
			return summ / size;
		}

		void znaki(int &minus, int &plus){

		    for (int i = 0; i < size; ++i){
				if (data[i] >= 0){
				    plus += 1;
				}
				else{
					minus += 1;
				}
			}
		}

		void print(){
			cout << "Массив: ";
			for (int i = 0; i < size; ++i){
				cout << data[i] << " ";
			}
			cout << "\n";
		}

		~massive() {
        	delete[] data;
    	}
};

int main()

{
//setlocale(LC_ALL, "rus");

int plus = 0;
int minus = 0;

massive A;

massive B {1, 2, 3};

A.znaki(minus, plus);
cout << "Количество элементов со знаком плюс : " << plus << "\n";
cout << "Количество элементов со знаком минус : " << minus << "\n";
cout << "Среднее значение: " << A.srednee() << "\n";
A.print();
B.print();

return 0;

}