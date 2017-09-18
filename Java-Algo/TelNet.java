/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package aufgabe4;

import java.awt.Point;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Random;

/**
 *
 * @author rob
 */
public class TelNet {
    private Map<Integer,TelKnoten> telnet;
    private PriorityQueue<TelVerbindung> edges;
    private final int lbg;
    private int size;
    
    public TelNet(int lbg) {
        this.lbg = lbg;
        size = 0;
        telnet = new <Integer,TelKnoten>HashMap();
        edges = new PriorityQueue<TelVerbindung>();
    }
    
    public boolean addTelKnoten(int x, int y) {
        if (telnet.containsValue(new TelKnoten(x,y))) {
            return false;
        } else {
            TelKnoten node = new TelKnoten(x,y);
            for (int i=0; i < size; i++) {
                TelKnoten t = telnet.get(i);
                int cost = (int) Math.abs(t.x - node.x) + Math.abs(t.y - node.y);
                if (cost <= lbg) {
                    edges.add(new TelVerbindung(t,node,cost));
                }
            }
            
            
            
            telnet.put(size, node);
            size++;
            return true;
        }
    }
    
    private int getKey(TelKnoten t) {
        for (int i = 0; i < size; i++) {
            if (telnet.get(i).equals(t)) {
                return i;
            }
        }
        return -1;
    }
    
    public List<TelVerbindung> getOptTelNet() {
        UnionFind forest = new UnionFind(this.size);
        List<TelVerbindung> minSpanTree = new LinkedList<TelVerbindung>();
        PriorityQueue<TelVerbindung> edges_clone = new PriorityQueue<TelVerbindung>(edges);
        
        
        while(forest.size() != 1 && !edges_clone.isEmpty()) {
            TelVerbindung tmp_ver = edges_clone.poll();
            int t1 = forest.find(getKey(tmp_ver.v));
            int t2 = forest.find(getKey(tmp_ver.u));
            
            if(t1 != t2) {
                forest.union(t1, t2);
                minSpanTree.add(tmp_ver);
            }      
        }
        
        if (edges_clone.isEmpty() && forest.size() != 1) {
            return null;
        } else {
            return minSpanTree;
        }
    }
    
    public boolean computeOptTelNet() {
        List<TelVerbindung> opt = getOptTelNet();
        return opt != null;
    }
    
    public int getOptTelNetKosten() {
        List<TelVerbindung> opt = getOptTelNet();
        if (opt == null) {
            return -1;
        } else {
            int sum = 0;
            for (TelVerbindung opt1 : opt) {
                sum += opt1.c;
            }
            return sum;
        }
    }
    
    public void drawOptTelNet(int xMax, int yMax) {
        if(!computeOptTelNet()) {
            return;
        }
        StdDraw.setXscale(0, xMax);
        StdDraw.setYscale(0, yMax);
        StdDraw.setPenRadius(0.01);
        for (int i = 0; i < size; i++) {
            TelKnoten t = telnet.get(i);
            StdDraw.setPenColor(StdDraw.BLACK);
            StdDraw.point(t.x, t.y);
        }
        
        List<TelVerbindung> opt = getOptTelNet();
        StdDraw.setPenColor(StdDraw.RED);
        StdDraw.setPenRadius(0.0025);
        for (TelVerbindung opt1 : opt) {
            
            StdDraw.line(opt1.u.x, opt1.u.y, opt1.u.x, opt1.v.y);
            StdDraw.line(opt1.u.x, opt1.v.y, opt1.v.x, opt1.v.y);
        }
        
    }
    
    public void generateRandomTelNet(int n, int xMax, int yMax) {
        Random rand = new Random();
        while(!computeOptTelNet()) {
            for (int i = 0; i < n; i++) {
                while (!addTelKnoten(rand.nextInt(xMax+1),rand.nextInt(yMax+1))) {
                    //do nothing
                }
            }
        }
    }
    
    public int size() {
        return size;
    }
    
    @Override
    public String toString() {
        String holder = "";
        for (int i = 0; i < size; i++) {
            holder += "\nNode " + Integer.toString(i) + ": " + telnet.get(i).toString();
        }
        return holder;
    }
    
    public static void main(String[] args) {
        
        /*
        tmp.addTelKnoten(1, 1);
        tmp.addTelKnoten(3,1);
        tmp.addTelKnoten(4,2);
        tmp.addTelKnoten(3,4);
        tmp.addTelKnoten(2,6);
        tmp.addTelKnoten(4,7);
        tmp.addTelKnoten(7,5);

        System.out.println(tmp.computeOptTelNet());
        System.out.println(tmp.getOptTelNetKosten());
        List<TelVerbindung> tmp_list = tmp.getOptTelNet();
        System.out.println(tmp_list);
        
        tmp.drawOptTelNet(20, 20);
        
        
        System.out.println(tmp.toString());
        System.out.println(tmp.size);
        */
        TelNet tmp = new TelNet(100);
        tmp.generateRandomTelNet(1500, 1500, 1500);
        tmp.drawOptTelNet(1500,1500);
    }
    
}
