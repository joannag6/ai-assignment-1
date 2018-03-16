#include <stdio.h>
#include <stdlib.h>

// Cute definitions to adhere to good C style, tq Alistair. 
#define TRUE 1
#define FALSE 0

//Function parameters. 
int calcMoves(int i, int j, char board[8][8]);
void printScore (int w, int b);
int checkDown(); 
int checkRight(); 
int checkLeft(); 
int checkUp(); 
void readIntoBoard(char board[8][8]); 
void printBoard(char board[8][8]); 
int firstRowMoves(int i,int j,char board[8][8]);
int lastRowMoves(int i,int j,char board[8][8]);
int leftColMoves(int i,int j,char board[8][8]);
int rightColMoves(int i,int j,char board[8][8]); 
int outOfBounds(int i, int j); 
int checkPiecePresence(char piece);
int checkJumpLeft(int i, int j, char board[8][8]);
int checkJumpUp(int i, int j, char board[8][8]);
int checkJumpRight(int i, int j, char board[8][8]);
int checkJumpDown(int i, int j, char board[8][8]);
void readOrder(); 

int
main(int argc, char* argv[]){
	// Declare useful i and j.
	int i = 0, j = 0;  
	// Declare board!
	char board[8][8]; 
	//Read into board. 
	readIntoBoard(board); 
	//Test if it was read correctly. 
	//TODO delte. 
	printBoard(board); 
	//Now read Move or Massacre. 
	readOrder(); 
	//Now, we have crude algorithm to calculate every move. 
	char currentchar = 'a';
	int whiteMoves = 0; 
	int blackMoves = 0; 
	for(i = 0; i<8; i++){
		for(j = 0; j<8; j++){
			currentchar = board[i][j];
			if(currentchar=='O'){
				whiteMoves += calcMoves(i,j, board);
				//printf("\n WHITEPIECE FOUND ON [%d][%d]", i, j);
				//printf("\n possible moves for this one is %d", calcMoves(i,j,board));
			}else if(currentchar == '@'){
				blackMoves += calcMoves(i,j, board);
				//printf("\n BLACKPIECE FOUND ON [%d][%d]", i, j); 
				//printf("\n possible moves for this one is %d", calcMoves(i,j,board));
			}
		}
	}
	
	for(i = 0; i<8; i++){
		for ( j = 0; j<8; j++){
				//printf("this is a stupid debug message, [%d][%d] is %c\n ", i, j, board[i][j]);
		}
		//printf("\n");
	}
	printScore(whiteMoves, blackMoves); 

	return 0; 
}

void readIntoBoard(char board[8][8]){
	char currentchar = 'a'; 
	int i = 0, j = 0; 
	// Function that reads in. 
	while(i<8){
		currentchar = getchar(); 
		if(currentchar =='X' || currentchar == '@' || 
			currentchar == '-' || currentchar == 'O'){
			board[i][j] = currentchar; 
			j++; 
		}
		if(currentchar == '\n'){
			i++; j = 0; 
		}
	} 
}

//Some hacky shit, you can just ignore it. 
void readOrder(){
	getchar(); 
	char x = getchar(); 
	if(x=='o'){
		printf("\nTHE DIRECTIVE IS MOVE!"); 
		return;
	}
	if(x == 'a'){
		printf("\nTHE DIRECTIVE IS MASSACRE!"); 
		return; 
	}
	exit(EXIT_FAILURE); 
}

void printBoard(char board[8][8]){
	int i = 0, j = 0; 
	for(i = 0; i<8; i++){
		printf("\n"); 
		for ( j = 0; j<8; j++){
			printf("%c", board[i][j]);
			printf(" "); 
		}
	}	
}

int calcMoves(int i, int j, char board[8][8]){
	int possibleMoves = 0; 
	if(i == 0){
		// if i = 0, we are in first row.
		possibleMoves += firstRowMoves(i,j,board); 
	}
	else if(i == 7){
		// if i = 7, we are in last row. 
		possibleMoves += lastRowMoves(i,j,board); 
	}
	else if( j == 0){
		// if j = 0, we are on the leftmost col, 
		possibleMoves += leftColMoves(i,j,board);
	
	}
	else if( j == 7){
		// if j = 7, we are on the rightmost col, 
		possibleMoves += rightColMoves(i,j,board);
	}
	else{
		//check all directions
		possibleMoves += checkLeft(i,j,board);
		possibleMoves += checkDown(i,j,board);
		possibleMoves += checkRight(i,j,board);
		possibleMoves += checkUp(i,j,board); 
	
		//Now we check for jumps.
		possibleMoves += checkJumpLeft(i,j,board);
		possibleMoves += checkJumpDown(i,j,board);
		possibleMoves += checkJumpUp(i,j,board);
		possibleMoves += checkJumpRight(i,j,board);
	}
	return possibleMoves; 
}

int firstRowMoves(int i, int j, char board[8][8]){
		int possibleMoves = 0; 
		//First check if we can move to any immediate squares. 
		//First row will check left, down, right. 
		possibleMoves += checkLeft(i,j,board);
		possibleMoves += checkDown(i,j,board);
		possibleMoves += checkRight(i,j,board); 
		
		//Now we check for jumps. 
		possibleMoves += checkJumpLeft(i,j,board);
		possibleMoves += checkJumpDown(i,j,board);
		possibleMoves += checkJumpRight(i,j,board);

		return possibleMoves; 
}



int lastRowMoves(int i, int j, char board[8][8]){
		int possibleMoves = 0; 
		//First check if we can move teo any immediate squares. 
		//If i = 7, we check left, right, up, for immediate moves. 
		possibleMoves += checkLeft(i,j,board);
		possibleMoves += checkRight(i,j,board);
		possibleMoves += checkUp(i,j,board);

		//Now we check for jumps. 
		possibleMoves += checkJumpLeft(i,j,board);
		possibleMoves += checkJumpRight(i,j,board);
		possibleMoves += checkJumpUp(i,j,board);
		return possibleMoves; 
}

int leftColMoves(int i, int j, char board[8][8]){
		int possibleMoves = 0; 
		// check up, right, down. 
		possibleMoves += checkUp(i,j,board);
		possibleMoves += checkRight(i,j,board);
		possibleMoves += checkDown(i,j,board);	

		//Now we check for jumps. 
		possibleMoves += checkJumpUp(i,j,board);
		possibleMoves += checkJumpRight(i,j,board);
		possibleMoves += checkJumpDown(i,j,board);

		return possibleMoves; 
}

int rightColMoves(int i, int j, char board[8][8]){
	int possibleMoves = 0; 
	//check up, left, down. 
	possibleMoves += checkUp(i,j,board);
	possibleMoves += checkLeft(i,j,board);
	possibleMoves += checkDown(i,j,board);		

	//Now we check for jumps. 
	possibleMoves += checkJumpUp(i,j,board);
	possibleMoves += checkJumpLeft(i,j,board);
	possibleMoves += checkJumpDown(i,j,board);
	return possibleMoves; 
}

int checkRight(int i, int j, char board[8][8]){
	if(board[i][j+1] == '-'){
		return 1; 
	}
	return 0;
}

int checkUp(int i, int j, char board[8][8]){
	if(board[i-1][j] == '-'){
		return 1; 
	}
	return 0; 
}

int checkDown(int i, int j, char board[8][8]){
	if(board[i+1][j] == '-'){
		return 1; 
	}
	return 0; 
}

int checkLeft(int i, int j, char board[8][8]){
	if(board[i][j-1] == '-'){
		return 1; 
	}
	return 0;
}

int checkJumpLeft(int i, int j, char board[8][8]){
	// if jump target is out of bounds, we cannot jump. 
	if (outOfBounds(i,j-2)){
		return 0; 
	}
	//if not out of bounds, 
	// if piece on left. 
	// we can jump. 
	if(checkPiecePresence(board[i][j-1])){
		return 1; 
	}
	return 0;
}

int checkJumpRight(int i, int j, char board[8][8]){
	// if jump target is out of bounds, we cannot jump. 
	if (outOfBounds(i,j+2)){
		return 0; 
	}
	//if not out of bounds, 
	// if piece on right 
	// we can jump. 
	if(checkPiecePresence(board[i][j+1])){
		return 1; 
	}
	return 0;	
}

int checkJumpUp(int i, int j, char board[8][8]){
	// if jump target is out of bounds, we cannot jump. 
	if (outOfBounds(i-2,j)){
		return 0; 
	}
	//if not out of bounds, 
	// if piece on up side 
	// we can jump. 
	if(checkPiecePresence(board[i-1][j])){
		return 1; 
	}
	return 0;
}

int checkJumpDown(int i, int j, char board[8][8]){
	// if jump target is out of bounds, we cannot jump. 
	if (outOfBounds(i+2,j)){
		return 0; 
	}
	//if not out of bounds, 
	// if piece on down
	// we can jump. 
	if(checkPiecePresence(board[i+1][j])){
		return 1; 
	}
	return 0;
}

// if i or j is <0 or >7, we have an out of bound cell. 
int outOfBounds(int i, int j){
	if (i < 0 || i>7 || j<0 || j>7){
		return TRUE; 
	}
	return FALSE; 
}


// Check if the char is representing a piece. 
int checkPiecePresence(char piece){
	if (piece == '@' || piece == 'O'){
		return TRUE; 
	}
	return FALSE;
}

void printScore(int w, int b){
	printf("\n%d\n%d", w, b);
}