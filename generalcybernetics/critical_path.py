from generalcybernetics.basis import Element, System


def test():

	a1 = Element(payload=2)
	b1 = Element(payload=1)
	c1 = Element(payload=2)

	a2 = Element(payload=2)
	b2 = Element(payload=5)

	a3 = Element(payload=1)

	a1.connect_lr(a2)
	b1.connect_lr(b2)
	c1.connect_lr(b2)

	a2.connect_lr(a3)
	b2.connect_lr(a3)

	inits = [a1, b1, c1]
	node_d,timedata,longest_path = calculate_critical_path(inits)
	#for x in priorities:
		#print(x)
	for key in timedata:
		print(key,timedata[key])
	print("path")
	print(longest_path)
	for x in longest_path:
		print(x,timedata[x])
	print("")

def test2():

	a1 = Element(payload=2)

	a2 = Element(payload=2)
	b2 = Element(payload=5)
	c2 = Element(payload=4)
	c21 = Element(payload=4)
	
	a3 = Element(payload=1)

	a1.connect_lr(a2)
	a1.connect_lr(b2)
	a1.connect_lr(c2)

	c2.connect_lr(c21)

	a2.connect_lr(a3)
	b2.connect_lr(a3)
	c21.connect_lr(a3)

	inits = [a1]
	node_d,timedata,longest_path = calculate_critical_path(inits)
	#for x in priorities:
		#print(x)
	for key in timedata:
		print(key,timedata[key])
	print("path")
	print(longest_path)
	for x in longest_path:
		print(x,timedata[x])
	print("")


def calculate_latest_end(inits,node_d,timedata):
	"""
	traverses the whole graph and figures out end times for the nodes
	"""
	current_nodes = []
	next_nodes = inits
	while len(next_nodes)>0:
		current_nodes = next_nodes
		next_nodes = []
		for node in current_nodes:
			nodeid = id(node)
			timedata[nodeid]["end"] = timedata[nodeid]["start"] + timedata[nodeid]["duration"]
			for out in node.out_connections:
				if timedata[nodeid]["end"] > timedata[id(out)]["start"]:
					timedata[id(out)]["start"] = timedata[nodeid]["end"]
			
			
			for x in node.out_connections:
				if x not in next_nodes:
					next_nodes.append(x)
	return timedata

def get_duration_times(inits,evaluation_function):
	"""
	traverses the whole graph,
	initializes the timedata dict and calculates the length of operations
	"""
	timedata = {}
	node_d = {}

	current_nodes = []
	next_nodes = inits
	while len(next_nodes)>0:
		current_nodes = next_nodes
		next_nodes = []
		for node in current_nodes:
			nodeid = id(node)
			if nodeid not in node_d:
				node_d[nodeid]=node
			duration=0
			if nodeid not in timedata:
				if evaluation_function is None:
					duration += node.payload
				else:
					duration += evaluation_function(node.payload)
				timedata[nodeid]={"start":0,"duration":duration,"end":0}
			
			for x in node.out_connections:
				if x not in next_nodes:
					next_nodes.append(x)
	
	return node_d, timedata

def find_last_end(timedata):
	"""
	finds the node with the longest end time, for backwards searching
	"""
	longest_path = []
	
	last_finish = 0
	last_finish_id = None
	for nodeid in timedata:
		if timedata[nodeid]["end"] > last_finish:
			last_finish=timedata[nodeid]["end"]
			last_finish_id=nodeid
			
	longest_path.append(last_finish_id)
	return longest_path

def breadth_first_backwards(node_d,timedata,longest_path):
	"""
	performs the backwards search to find the longest path through
	my network
	"""
	last_finish_id = longest_path[0]
	while True:
		last_finish = 0
		my_node = node_d[last_finish_id]
		last_finish_id = None
		for x in my_node.in_connections:
			if timedata[id(x)]["end"] > last_finish:
				last_finish = timedata[id(x)]["end"]
				last_finish_id = id(x)
		if last_finish_id==None:
			break
		
		if last_finish_id not in longest_path:
			longest_path.append(last_finish_id)
	
	longest_path.reverse()
	return longest_path

def calculate_critical_path(inits, evaluation_function=None):
	"""
	if the eval function is None, I assume it's a number or number like
	otherwise evaluation_function(Node.payload) will be added to the path
	cost
	
	inits could be found automatically by finding elements without inputs.
	"""

	node_d,timedata = get_duration_times(inits,evaluation_function)
	timedata = calculate_latest_end(inits,node_d,timedata)
	longest_path = find_last_end(timedata)
	longest_path = breadth_first_backwards(node_d,timedata,longest_path)
	
	return node_d,timedata,longest_path


if __name__ == "__main__":
	test()
	test2()
