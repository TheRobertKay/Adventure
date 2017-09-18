/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package aufgabe4;

/**
 *
 * @author rob
 */
public class TelVerbindung implements Comparable<TelVerbindung>{
    public final TelKnoten u;
    public final TelKnoten v;
    public final int c;   
    
    public TelVerbindung(TelKnoten u, TelKnoten v, int c) {
        this.u = u;
        this.v = v;
        this.c = c;
    }
    
    @Override
    public String toString() {
        String holder = String.format("%d:%d <-> %d:%d [%d]",u.x,u.y,v.x,v.y,c);
        return holder;
    }
    
    @Override
    public int compareTo(TelVerbindung o) {
        return this.c - o.c;
    }
}
