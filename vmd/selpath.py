# Draw the path of an atom selection

def avg(a):
  ans=0
  for x in a:
    ans += x
  return ans/len(a)

from VMD import graphics, molecule
def selpath(sel, color='blue'):
  id=sel.molid()
  sel.frame(0)
  x,y,z = sel.get('x', 'y', 'z')
  a1 = avg(x), avg(y), avg(z)
  graphics.delete(id, 'all')
  graphics.color(id, color)
  nframes = molecule.numframes(id)
  for frame in range(1, nframes):
    sel.frame(frame)
    x,y,z = sel.get('x', 'y', 'z')
    a2 = avg(x), avg(y), avg(z)
    graphics.line(id, a1, a2)
    a1 = a2

if __name__=="__main__":
  from VMD import AtomSel
  sel=AtomSel.AtomSel('resid 1')
  selpath(sel)
