package com.mobilechaos.www;

import android.content.Context;
import android.support.v7.widget.AppCompatTextView;
import android.util.AttributeSet;

import java.util.ArrayList;

public class SwipeableTextView extends AppCompatTextView {


    private ArrayList<CharSequence> history;
    private int historyViewIndex = 0;

    public SwipeableTextView(Context context) {
        super(context);
        history = new ArrayList<CharSequence>();
    }
    public SwipeableTextView(Context context, AttributeSet attrs) {
        super(context,attrs);
        history = new ArrayList<CharSequence>();
    }
    public SwipeableTextView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        history = new ArrayList<CharSequence>();
    }

    public int getIndex() {return historyViewIndex;}
    public void setIndex(int index) {historyViewIndex = index;}

    public boolean decrementHistory() {
        if(historyViewIndex > 0){
            historyViewIndex--;
            this.setText(getHistoryItem(historyViewIndex));
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
            this.setText(getHistoryItem(historyViewIndex));
            return true;
        }
    }

    public void setHistory(ArrayList<CharSequence> history) {
        this.history = history;
    }

    public void addHistory(String string){
        history.add(string);
        historyViewIndex = history.size()-1;
    }

     public CharSequence getHistoryItem(int index){
         if (history.isEmpty())
             return null;
         else
             return history.get(index);

     }

     protected ArrayList<CharSequence> getHistory()
     {
         return history;
     }

    public CharSequence getCurrent(){
        if (history.isEmpty())
            return null;
        else
            return history.get(history.size()-1);
    }

    public void updateHistoryItem(String string, int idx){
        if (!history.isEmpty())
            history.set(idx, string);
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
