// Startnode script
match (n) where ID(n)=0 
SET n.name="startnode"
RETURN n;
