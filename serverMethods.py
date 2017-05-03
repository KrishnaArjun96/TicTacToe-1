def respond_to_client(player, message, connectionSocket):
	connectionSocket.sendto(message, player.get_address())