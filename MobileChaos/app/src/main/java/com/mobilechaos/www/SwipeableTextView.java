package com.mobilechaos.www;

import android.content.Context;
import android.support.v7.widget.AppCompatTextView;
import android.util.AttributeSet;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;

public class SwipeableTextView extends AppCompatTextView {


    private ArrayList<String> history;
    private int historyViewIndex = 0;

    public boolean decrementHistory() {
        if(historyViewIndex > 0){
            historyViewIndex--;
            this.setText(getHistory(historyViewIndex));
            return true;
        }
        else {
            return false;
        }
    }
    public boolean incrementHistory() {
        if(historyViewIndex >= (history.size() - 1))
            return false;
        else {
            historyViewIndex++;
            this.setText(getHistory(historyViewIndex));
            return true;
        }
    }

    public ArrayList<String> getHistory() {
        return history;
    }

    public void setHistory(ArrayList<String> history) {
        this.history = history;
    }

    public void addHistory(String string){
        history.add(string);
        historyViewIndex = history.size()-1;
    }

     public String getHistory(int index){
         if (history.isEmpty())
             return null;
         else
             return history.get(index);

     }

    public String getCurrent(){
        if (history.isEmpty())
            return null;
        else
            return history.get(history.size()-1);
    }

    public void updateCurrent(String string){
        if (!history.isEmpty())
            history.set(history.size()-1, string);
    }

    public SwipeableTextView(Context context) {
        super(context);
        history = new ArrayList<String>();
    }
    public SwipeableTextView(Context context, AttributeSet attrs) {
        super(context,attrs);
        history = new ArrayList<String>();
    }
    public SwipeableTextView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context,attrs, defStyleAttr);
        history = new ArrayList<String>();
    }

    /*
    SwipeableTextView(Context context, AttributeSet attrs, int defStyleAttr, int defStyleRes) {
        super(context, attrs, defStyleAttr, defStyleRes);
    }
    */

    @Override
    public boolean performClick() {
        return super.performClick();
    }
}
