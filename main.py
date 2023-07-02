from math import floor, log2
from random import randint
from time import perf_counter
from typing import Callable, List

sort: Callable[[ List[int] ], List[int]] = lambda a: a.sort() or a

class Node:
	def __init__(self, value: int = 0):
		self.value: int = value
		self.parent: Node|None = None
		self.left_child: Node|None = None
		self.right_child: Node|None = None
		self.height: int = 1

class BST:
	def __init__(self, values: List[int]):
		self.root: Node|None = None
		for v in values:
			self.insert( v )

	def _insert(self, value: int, current_node: Node):
		if value<current_node.value:
			if current_node.left_child==None:
				current_node.left_child=Node(value)
				current_node.left_child.parent=current_node
			else:
				self._insert(value,current_node.left_child)
		elif value>current_node.value:
			if current_node.right_child == None:
				current_node.right_child = Node(value)
				current_node.right_child.parent=current_node
			else:
				self._insert(value, current_node.right_child)
		else:
			return False


	def insert(self, value: int):
		if self.root==None:
			self.root=Node(value)
		else:
			self._insert(value,self.root)

	def _in_order(self,current_node: Node|None):
		if current_node!=None:
			self._in_order(current_node.left_child)
			print(current_node.value, end=' ')
			self._in_order(current_node.right_child)

	def in_order(self):
		if self.root != None:
			self._in_order(self.root)

	def _height(self, current_node: Node|None, current_height: int) -> int:
		if current_node==None:
			return current_height
		left_height=self._height(current_node.left_child,current_height+1)
		right_height=self._height(current_node.right_child,current_height+1)
		return max(left_height,right_height)

	def height(self) -> int:
		if self.root != None:
			return self._height(self.root,0)
		else:
			return 0

	def _find_max(self,current_node: Node) -> int:
		if current_node.right_child != None:
			print( f'{ current_node.value } -> ', end='' )
			return self._find_max(current_node.right_child)
		return current_node.value

	def find_max(self):
		if self.root != None:
			return self._find_max(self.root)
		else:
			return False

	def _find_min(self, current_node: Node) -> int:
		if current_node.left_child != None:
			print( f'{ current_node.value } -> ', end='' )
			return self._find_min(current_node.left_child)
		return current_node.value

	def find_min(self):
		if self.root != None:
			return self._find_min(self.root)
		else:
			return False

	def _find(self, value: int, current_node: Node) -> Node|None:
		if value==current_node.value:
			return current_node
		elif value>current_node.value and current_node.right_child!=None:
			return self._find(value,current_node.right_child)
		elif value<current_node.value and current_node.left_child!=None:
			return self._find(value,current_node.left_child)

	def find(self, value: int):
		if self.root != None:
			return self._find(value,self.root)
		else:
			return None

	def del_node(self,node: Node):
		def children_number(pom: Node):
			res=0
			if pom.left_child != None:
				res+=1
			if pom.right_child != None:
				res+=1
			return res
		def _min(current: Node) -> Node:
			if current.left_child != None:
				return _min(current.left_child)
			return current

		node_parent=node.parent
		node_children=children_number(node)

		if node_children == 0:
			if node_parent == None:
				self.root = None
			elif node_parent.left_child==node:
				node_parent.left_child=None
			else:
				node_parent.right_child=None
		if node_children == 1:
			if node.left_child!=None:
				child=node.left_child
			else:
				child=node.right_child

			if node_parent == None:
				self.root = child
			elif node_parent.left_child==node:
				node_parent.left_child=child
			else:
				node_parent.right_child=child
			child.parent=node_parent  # type: ignore
		if node_children == 2:
			succes=_min(node.right_child)  # type: ignore
			node.value=succes.value

			self.del_node(succes)

	def del_value(self, value: int):
		node = self.find(value)
		if node != None:
			return self.del_node( node )

	def _pre_order(self, current_node: Node|None):
		if current_node != None:
			print(current_node.value, end=' ')
			self._pre_order(current_node.left_child)
			self._pre_order(current_node.right_child)

	def pre_order(self):
		if self.root != None:
			self._pre_order(self.root)
	def pre_order_node(self, current_node: Node|None):
		self._pre_order( current_node )

	def _post_order_del(self, current_node: Node|None):
		if current_node != None:
			self._post_order_del(current_node.left_child)
			current_node.left_child = None
			self._post_order_del(current_node.right_child)
			current_node.right_child = None
			print(current_node.value, end=' ')

	def post_order_del(self):
		if self.root != None:
			self._post_order_del(self.root)
			self.root = None

	def _dsw(self, node: Node|None):
		if node == None:
			return

		while node.left_child != None:
			self._right_rotate( node )

		self._dsw( node.right_child )

	def dsw(self):
		def compress( node: Node, count: int ):
			cur = node
			for _ in range( 0, count ):
				child = cur.right_child
				cur.right_child = child.right_child
				if cur.right_child:
					cur.right_child.parent = cur

				cur = cur.right_child
				child.right_child = cur.left_child
				if child.right_child:
					child.right_child.parent = child

				cur.left_child = child
				child.parent = cur

		if self.root != None:
			cur = self.root
			while cur != None:
				if cur.left_child != None:
					self._right_rotate( cur )
					cur = cur.parent
				else:
					cur = cur.right_child

			s = self.height()
			l = s + 1 - pow( 2, floor(log2( s + 1 ) ) )
			root = Node( 0 )
			root.right_child = self.root
			self.root.parent = root
			compress( root, l )
			s -= l
			while s > 1:
				s //= 2
				compress( root, s )
			self.root = root.right_child
			self.root.parent = None 
		else:
			return False

	def _left_rotate(self,a: Node):
		pom_root = a.parent
		b = a.right_child
		r2 = b.left_child
		b.left_child = a
		a.parent = b
		a.right_child = r2
		if r2 != None:
			r2.parent = a
		b.parent = pom_root
		if b.parent == None:
			self.root = b
		else:
			if b.parent.left_child == a:
				b.parent.left_child = b
			else:
				b.parent.right_child = b
		a.height = 1 + max(self.get_height(a.left_child), self.get_height(a.right_child))
		b.height = 1 + max(self.get_height(b.left_child), self.get_height(b.right_child))

	def _right_rotate(self,a: Node):
		pom_root=a.parent
		b=a.left_child
		r2=b.right_child
		b.right_child=a
		a.parent=b
		a.left_child=r2
		if r2!=None:
			r2.parent=a
		b.parent=pom_root
		if b.parent== None:
			self.root=b
		else:
			if b.parent.left_child==a:
				b.parent.left_child=b
			else:
				b.parent.right_child=b
		a.height=1+max(self.get_height(a.left_child), self.get_height(a.right_child))
		b.height=1+max(self.get_height(b.left_child), self.get_height(b.right_child))

	def get_height(self, current_node: Node|None):
		if current_node == None:
			return 0
		return current_node.height

class AVL(BST):
	def __init__(self, values: List[int]):
		self.root: Node|None = None
		# values.sort()

		def insertvalues( values: List[int] ):
			if len( values ) > 0:
				i = len( values ) // 2 + len( values ) % 2 - 1
				self.insert( values.pop( i ) )
				left = values[:i]
				right = values[i:]
				insertvalues( left )
				insertvalues( right )
		insertvalues( values )
		pass

	def _insert(self, value: int, current_node: Node):
		if value<current_node.value:
			if current_node.left_child == None:
				current_node.left_child = Node(value)
				current_node.left_child.parent = current_node
				#self._insp_insert(current_node.left_child)
			else:
				self._insert(value,current_node.left_child)
		elif value>current_node.value:
			if current_node.right_child == None:
				current_node.right_child = Node(value)
				current_node.right_child.parent=current_node
				#self._insp_insert(current_node.right_child)

			else:
				self._insert(value, current_node.right_child)
		else:
			return False

	def del_node(self, node: Node):
		def children_number(pom: Node):
			res=0
			if pom.left_child != None:
				res+=1
			if pom.right_child != None:
				res+=1
			return res
		def _min(current: Node) -> Node:
			if current.left_child != None:
				return _min(current.left_child)
			return current

		node_parent=node.parent
		node_children=children_number(node)

		if node_children == 0:
			if node_parent == None:
				self.root = None
			elif node_parent.left_child==node:
				node_parent.left_child=None
			else:
				node_parent.right_child=None
		if node_children == 1:
			if node.left_child!=None:
				child=node.left_child
			else:
				child=node.right_child

			if node_parent == None:
				self.root = None
			elif node_parent.left_child==node:
				node_parent.left_child=child
			else:
				node_parent.right_child=child
			child.parent=node_parent # type: ignore
		if node_children == 2:
			succes=_min(node.right_child) # type: ignore
			node.value=succes.value

			self.del_node(succes)

			return

		if node_parent != None:
			node_parent.height=1+max(self.get_height(node_parent.left_child),
			self.get_height(node_parent.right_child))

			self._insp_del(node_parent)

	def _insp_insert(self, current_node: Node|None, path:List[Node]=[]):
		if current_node==None:
			return False
		path=[current_node]+path

		left_height = self.get_height(current_node.parent.left_child)
		right_height = self.get_height(current_node.parent.right_child)

		if abs(left_height-right_height)>1:
			path=[current_node.parent]+path
			self._node_rebalance(path[0],path[1],path[2])
			return
		new_height=1+current_node.height
		if new_height>current_node.parent.height:
			current_node.parent.height=new_height

	def _insp_del(self,current_node: Node):
		if current_node.parent==None: return

		left_height = self.get_height(current_node.parent.left_child)
		right_height = self.get_height(current_node.parent.right_child)

		if abs(left_height - right_height) > 1:
			b=self.taller_child(current_node)
			c=self.taller_child(b)
			self._node_rebalance(current_node,b,c)

		self._insp_del(current_node.parent)
	def _node_rebalance(self,a:Node,b:Node,c:Node):
		if b==a.left_child and c==b.left_child:
			self._right_rotate(a)
		elif b==a.left_child and c==b.right_child:
			self._right_rotate(a)
			self._left_rotate(b)
		elif b==a.right_child and c==b.right_child:
			self._left_rotate(a)
		elif b==a.right_child and c==b.left_child:
			self._right_rotate(b)
			self._left_rotate(a)
		else:
			return False

	def taller_child(self,current_node):
		left=self.height(current_node.left_child)
		right=self.height(current_node.left_child)
		if left>right:
			return current_node.left_child
		elif right>left:
			return current_node.right_child

def data(n: int,min: int|str,max: int|str) -> List[int]:
	tab: List[int] = []
	while len(tab) < n:
		pom=randint(int(min),int(max))
		if pom not in tab:
			tab.append(pom)
	return tab

#def filling(tree,num_el=100,max=1000):
#	for i in range(num_el):
#		pom=randint(0,max)
#		tree.insert(pom)
#	return tree

inputMethod: int = 0
while True:
	print( '\033cWczytaj dane:' )
	print( '1. Wygeneruj' )
	print( '2. Z klawiatury' )
	try:
		inputMethod = int( input( '>' ) )
		if inputMethod == 1 or inputMethod == 2:
			break
	except ValueError:
		pass
print( '\033c', end='' )

n = 0
arr: List[int] = []
while True:
	print( '\033cWczytaj dane:' )
	try:
		n = int( input( 'n = ' ) )
		if n > 0:
			break
	except ValueError:
		pass

if inputMethod == 2:
	for i in range( 1, n + 1 ):
		while True:
			print( '\033cWczytaj dane:' )
			try:
				v = int( input( f'node [{ i }/{ n }]>' ) )
				if v not in arr:
					arr.append( v )
					break
			except ValueError:
				pass
else:
	vmin = vmax = 0
	while True:
		print( '\033cWczytaj dane:' )
		try:
			vmin = int( input( 'min = ' ) )
			break
		except ValueError:
			pass
	while True:
		print( '\033cWczytaj dane:' )
		try:
			vmax = int( input( f'max (min: { vmin + n }) = ' ) )
			if vmax >= vmin + n:
				break
		except ValueError:
			pass
	arr = data(n, vmin, vmax )


print(arr)
input( '...' )
print( '\033cTworzenie drzewa:' )
print( 'AVL:' )
avlarr = sort(list(arr))
start = perf_counter()
treeAVL = AVL(avlarr)
end = perf_counter()
print( f'Tworzenie: { ( end - start ) * 1000000 } μs\n\nBST:' )
start = perf_counter()
treeBST = BST(arr)
end = perf_counter()
print( f'Tworzenie: { ( end - start ) * 1000000 } μs' )
input( '...' )

#arr = [ 5, 4, 6, 10, 9, 11 ]
while True:
	op = 0
	while True:
		print( '\033cOperacje:' )
		print( '1. Find min' )
		print( '2. Find max' )
		print( '3. Del val' )
		print( '4. In-order' )
		print( '5. Pre-order' )
		print( '6. Post-order del' )
		print( '7. Pre-order (subtree)' )
		print( '8. Rebalance tree' )

		try:
			op = int( input( '>' ) )
			if op >= 1 and op <= 8:
				break
		except ValueError:
			pass

	if op == 1:
		print( '\033cFind min' )
		print( 'AVL: ', end='' )
		start = perf_counter()
		print( treeAVL.find_min(), end='' )
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		print( 'BST: ', end='' )
		start = perf_counter()
		print( treeBST.find_min(), end='' )
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		input( '...' )
	elif op == 2:
		print( '\033cFind max' )
		print( 'AVL: ', end='' )
		start = perf_counter()
		print( treeAVL.find_max(), end='' )
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		print( 'BST: ', end='' )
		start = perf_counter()
		print( treeBST.find_max(), end='' )
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		input( '...' )
	elif op == 3:
		print( '\033cDel val' )
		n = 0
		val: List[int] = []
		while True:
			try:
				n = int( input( 'amount = ' ) )
				break
			except ValueError:
				pass
		while len( val ) < n:
			while True:
				try:
					val.append( int( input( f'v [{ len(val) + 1 }/{ n }] = ' ) ) )
					break
				except ValueError:
					pass
		print( 'AVL: ', end='' )
		start = perf_counter()
		for v in val:
			treeAVL.del_value( v )
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		print( 'BST: ', end='' )
		start = perf_counter()
		for v in val:
			treeBST.del_value( v )
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		input( '...' )
	elif op == 4:
		print( '\033cIn-order' )
		print( 'AVL: ', end='' )
		start = perf_counter()
		treeAVL.in_order()
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		print( 'BST: ', end='' )
		start = perf_counter()
		treeBST.in_order()
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		input( '...' )
	elif op == 5:
		print( '\033cPre-order' )
		print( 'AVL: ', end='' )
		start = perf_counter()
		treeAVL.pre_order()
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		print( 'BST: ', end='' )
		start = perf_counter()
		treeBST.pre_order()
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		input( '...' )
	elif op == 6:
		print( '\033cPost-order del' )
		print( 'AVL: ', end='' )
		start = perf_counter()
		treeAVL.post_order_del()
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		print( 'BST: ', end='' )
		start = perf_counter()
		treeBST.post_order_del()
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		input( '...' )
	elif op == 7:
		print( '\033cPre-order (subtree)' )
		v = 0
		while True:
			try:
				v = int( input( 'v = ' ) )
				break
			except ValueError:
				pass
		print( 'AVL: ', end='' )
		start = perf_counter()
		treeAVL.pre_order_node( treeAVL.find( v ) )
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		print( 'BST: ', end='' )
		start = perf_counter()
		treeBST.pre_order_node( treeBST.find( v ) )
		end = perf_counter()
		print( f'   { ( end - start ) * 1000000 } μs' )
		input( '...' )
	elif op == 8:
		print( '\033cRebalance tree' )
		print( 'AVL:\n  - before: ', end='' )
		treeAVL.pre_order()
		start = perf_counter()
		treeAVL.dsw()
		end = perf_counter()
		print( '\n  - after: ', end='' )
		treeAVL.pre_order()
		print( '' )
		print( f'  - time: { ( end - start ) * 1000000 } μs' )

		print( 'BST:\n  - before: ', end='' )
		treeBST.pre_order()
		start = perf_counter()
		treeBST.dsw()
		end = perf_counter()
		print( '\n  - after: ', end='' )
		treeBST.pre_order()
		print( '' )
		print( f'  - time: { ( end - start ) * 1000000 } μs' )
		input( '...' )

