#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif

#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>
#include <stdio.h>
#include <stdlib.h>

#pragma comment(lib, "Ws2_32.lib")

#define SOCKNUM 16383
#define STARTPORT 49152

int main() {
	WSADATA wsaData;
	int iResult;
	// Initialize Winsock
	printf("Portkeeping start...\n");
	iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
	if (iResult != 0) {
		printf("WSAStartup failed: %d\n", iResult);
		return 1;
	}
	
	SOCKET zombies[SOCKNUM];
	struct sockaddr_in addrs[SOCKNUM];
	bool killed[SOCKNUM] = { false };

	printf("Keeping %d ports\n", SOCKNUM);

	TRY:
	//int port = STARTPORT;
	int fail = 0;
	//InetPton(AF_INET, (PCWSTR)("192.168.0.1"), &addr.sin_addr.s_addr);

	for (int i = 0; i < SOCKNUM; i++) {
		if (killed[i])
			continue;

		zombies[i] = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
		if (zombies[i] == INVALID_SOCKET) {
			printf("port %d error at socket(): %ld\n", STARTPORT+i, WSAGetLastError());
			WSACleanup();
			return 1;
		}

		addrs[i].sin_family = AF_INET;
		addrs[i].sin_port = htons(STARTPORT+i);
		addrs[i].sin_addr.s_addr = INADDR_ANY;

		iResult = bind(zombies[i], (struct sockaddr*)&addrs[i], sizeof(addrs[i]));
		if (iResult == SOCKET_ERROR) {
			printf("\nport %d bind failed with error: %d\n", STARTPORT+i, WSAGetLastError());
			fail++;
			closesocket(zombies[i]);
			zombies[i] = INVALID_SOCKET;
			killed[i] = false;
		}
		else {
			killed[i] = true;
			printf("\rPort %d bound", STARTPORT+i);
			fflush(stdout);
		}
	}

	printf("\nFinished: %d ports checked, %d fails\n", SOCKNUM, fail);

	if (fail) {
		printf("Ready to retry?");
		system("pause");
		printf("\n----------------------\n");
		goto TRY;
	}

	system("pause");
	return 0;
}
