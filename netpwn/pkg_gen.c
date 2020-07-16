// Generate DNS request for injection directly on the wire (Homebrew stress test)
//
// Example packet (tcpdump -lnx -i eth2 port 53):
//
// 19:21:35.494916 IP 3.1.33.7.46035 > localhost.53: 65222+ A? google.com. (28)
//	0x0000:  4500 0038 b087 0000 4011 26ae c0a8 c845
//	0x0010:  18e2 01b0 b3d3 0035 0024 a3b5 fec6 0100
//	0x0020:  0001 0000 0000 0000 0667 6f6f 676c 6503
//	0x0030:  636f 6d00 0001 0001
//
// Packet break down
//
// Domain Name System (query)
//    [Response In: 1852]
//    Transaction ID: 0x241a
//    Flags: 0x0100 (Standard query)
//        0... .... .... .... = Response: Message is a query
//        .000 0... .... .... = Opcode: Standard query (0)
//        .... ..0. .... .... = Truncated: Message is not truncated
//        .... ...1 .... .... = Recursion desired: Do query recursively
//        .... .... .0.. .... = Z: reserved (0)
//        .... .... ...0 .... = Non-authenticated data OK: Non-authenticated data is unacceptable
//    Questions: 1
//    Answer RRs: 0
//    Authority RRs: 0
//    Additional RRs: 0
//    Queries
//        google.com: type A, class IN
//            Name: google.com
//            Type: A (Host address)
//            Class: IN (0x0001)
//
// How to use:
// -----------
// 1. Compile our program to generate the DNS payload
// 
// (sipher@utensil)(~/dnsstress)$ gcc gr2.c -o gr2
// 
// 2. Generate DNS payload
// 
// (sipher@utensil)(~/dnsstress)$ ./gr2
// (sipher@utensil)(~/dnsstress)$ hexdump -C dns.txt
// 00000000  24 1a 01 00 00 01 00 00  00 00 00 00 06 67 6f 6f  |$............goo|
// 00000010  67 6c 65 03 63 6f 6d 00  00 01 00 01              |gle.com.....|
// 0000001c
//  
// 3. Get the size of the request (Important for passing to hping3 -d paramater)
// 
// (sipher@utensil)(~/dnsstress)$ ls -lah |grep dns.txt
// -rw-rw-r--  1 striemer striemer   28 Apr 17 10:30 dns.txt
// (sipher@utensil)(~/dnsstress)$
//
// 4. Fire!!
// use --flood if you're brave. Use --rand-source to test state tables.
// (sipher@utensil)(~/dnsstress)$ sudo hping3 localhost --udp -V -p 53 --file /home/sipher/dnsstress/dns.txt -d 28 --fast
// 
// Alternate way to deliver the packets...
// 
// NOTE: Won't be as fast since it's not using raw sockets and it's waiting for reply.
// 
// (sipher@utensil)(~/dnsstress)$ nc -u localhost 53 < dns.txt


#include <stdio.h>

int main() {

	FILE *fp;

	fp=fopen("dns.txt", "w+");

	//fprintf(fp,"%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c",0x24,0x1a,0x01,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x06,0x67,0x6f,0x6f,0x67,0x6c,0x65,0x03,0x63,0x6f,0x6d,0x00,0x00,0x01,0x00,0x01);
	fprintf(fp,"%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c",0x42,0x3a,0x81,0x80,0x00,0x01,0x00,0x01,0x00,0x00,0x00,0x00,0x06,0x67,0x6f,0x6f,0x67,0x6c,0x65,0x03,0x63,0x6f,0x6d,0x00,0x00,0x01,0x00,0x01,0xc0,0x0c,0x00,0x01,0x00,0x01,0x00,0x00,0x00,0x87,0x00,0x04,0xac,0xd9,0x0b,0xae);

	fclose(fp);


//char* buf;
//int i;

// Transaction ID
//buf[i++] = 0x24;
//buf[i++] = 0x1a;

// Standard Query
//buf[i++] = 0x01;
//buf[i++] = 0x00;


//        0... .... .... .... = Response: Message is a query
//        .000 0... .... .... = Opcode: Standard query (0)
//        .... ..0. .... .... = Truncated: Message is not truncated
//        .... ...1 .... .... = Recursion desired: Do query recursively
//        .... .... .0.. .... = Z: reserved (0)
//        .... .... ...0 .... = Non-authenticated data OK: Non-authenticated data is unacceptable
//buf[i++] = 0x00;
//buf[i++] = 0x01;
//buf[i++] = 0x00;
//buf[i++] = 0x00;
//buf[i++] = 0x00;
//buf[i++] = 0x00;
//buf[i++] = 0x00;
//buf[i++] = 0x00;
//buf[i++] = 0x06;

// g = 67
// o = 6f
// o = 6f
// g = 67
// l = 6c
// e = 65
// . = 03 (END OF TEXT
// c = 63
// o = 6f
// m = 6d


// Let's try changing the query name to whatever we want.
// strcpy((buf + i), hostname);
// i = i + strlen(hostname);

// google.com
//buf[i++] = 0x67;
//buf[i++] = 0x6f;
//buf[i++] = 0x6f;
//buf[i++] = 0x67;
//buf[i++] = 0x6c;
//buf[i++] = 0x65;
//buf[i++] = 0x03;
//buf[i++] = 0x63;
//buf[i++] = 0x6f;
//buf[i++] = 0x6d;

// Type A and Class IN
//buf[i++] = 0x00;
//buf[i++] = 0x00;
//buf[i++] = 0x01;
//buf[i++] = 0x00;
//buf[i++] = 0x01;

}
