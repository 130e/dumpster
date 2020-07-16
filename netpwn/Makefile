source=src.cpp
exec=a
test_src=test.cpp

run:
	g++ -Wall -std=c++11 -O2 $(source) -lpthread -o $(exec) \
		&& ./$(exec)

compile:
	g++ -Wall -std=c++11 -O2 $(source) -lpthread -o $(exec)

clean:
	rm ./$(exec)
