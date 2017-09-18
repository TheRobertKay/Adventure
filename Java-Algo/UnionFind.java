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
public class UnionFind {
    int[] p;
    int size;
    public UnionFind(int n) {
        this.p = new int[n];
        this.size = n;
        for (int i = 0; i < n; i++) {
            this.p[i] = -1;
        }
    }
    
    public int find(int e) {
        if (p[e] < 0) {
            return e;
        } else {
            return find(p[e]);
        }
    }
    
    public void union(int s1, int s2) {
        if (p[s1] >= 0 || p[s2] >= 0) {
            return;
        }
        if (s1 == s2) {
            return;
        }
        
        if (-p[s1] < -p[s2]) {
            p[s1] = s2;
        } else {
            if (-p[s1] == -p[s2]) {
                p[s1]--;
            }
            p[s2] = s1;
        }
        size--;
    }
    
    public int size() {
        return size;
    }
    
    public static void main(String[] args) {
        UnionFind tmp = new UnionFind(10);
        tmp.union(1, 4);
        tmp.union(3,1);
        tmp.union(2,5);
        tmp.union(tmp.find(2), tmp.find(1));
        for (int i = 0; i < tmp.p.length; i++) {
            System.out.printf("%d <-> %d\n",i,tmp.p[i]);
        }
        System.out.println(tmp.find(2));
    }
}
