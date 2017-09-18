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
public class TelKnoten {
    public final int x;
    public final int y;
    public TelKnoten(int x, int y) {
        this.x = x;
        this.y = y;
    }
    
    @Override
    public String toString() {
        return "x: " + Integer.toString(x) + " y: " + Integer.toString(y);
    }
}
