build:
	rpcgen -NC oauth.x
	g++ -g -o server server.cpp oauth_svc.cpp oauth_xdr.c -lnsl
	g++ -g -o client client.cpp oauth_clnt.c oauth_xdr.c -lnsl

full_clean:
	rm *.c oauth.h client server Makefile.oauth

clean:
	rm client server

first_build:
	rpcgen -aNC oauth.x