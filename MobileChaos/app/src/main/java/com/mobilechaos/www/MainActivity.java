package com.mobilechaos.www;

import java.io.FileNotFoundException;

import java.io.IOException;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserFactory;

import android.app.Activity;
import android.graphics.Typeface;
import android.os.Bundle;

import android.text.method.ScrollingMovementMethod;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import java.util.*;



public class MainActivity extends Activity {

    private static final String TAG = "MainActivity";
    private static final String STATE_CHAOS = "chaos";
    private static final String STATE_GLOBAL = "global";

    private Random random;

    public class ChaosRoll {

        public String rollName;
        public String rollEffect;
        public int rollWeight;

        public ChaosRoll(String name, String effect, int weight) {
            rollName = name;
            rollEffect = effect;
            rollWeight = weight;
        }
    }

    public class ChaosList {

        public String listName;
        public List<ChaosRoll> roll;
        public int totalWeight;

        public ChaosList(String list) {
            listName = list;
            roll = new ArrayList<ChaosRoll>();
            totalWeight = 0;
        }

        public void addRoll(String name, String effect, int weight)
        {
            roll.add(new ChaosRoll(name, effect, weight));
            totalWeight += weight;
        }

        public ChaosRoll getRandom() {

            int count = 0, dieRoll = random.nextInt(totalWeight);

            for (ChaosRoll croll : roll)
            {
                count += croll.rollWeight;
                if (dieRoll <= count) {
                    return croll;
                }
            }

            Toast.makeText(MainActivity.this, "Error: totalWeight (" + totalWeight + ") smaller than total of weights.", Toast.LENGTH_SHORT).show();

            return null;
        }
    }

    private List<String> listNames;
    private List<ChaosList> lists;
    private ChaosList global;

    private Spinner chaosSpinner;
    private Button chaosButton;
    private Button globalButton;

    private TextView chaosText;
    private TextView globalText;

    private Typeface customFont;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        customFont = Typeface.createFromAsset(getAssets(),  "fonts/Beleren-Bold.ttf");

        chaosSpinner = (Spinner) findViewById(R.id.listSpinner);

        chaosButton = (Button) findViewById(R.id.listButton);
        globalButton = (Button) findViewById(R.id.globalButton);

        chaosButton.setTypeface(customFont);
        globalButton.setTypeface(customFont);

        random = new Random();

        chaosText = (TextView) findViewById(R.id.chaosRollTextBox);
        globalText = (TextView) findViewById(R.id.globalTextBox);

        chaosText.setTypeface(customFont);
        globalText.setTypeface(customFont);

        chaosText.setMovementMethod(new ScrollingMovementMethod());
        globalText.setMovementMethod(new ScrollingMovementMethod());

        listNames = new ArrayList<String>();
        lists = new ArrayList<ChaosList>();
        global = new ChaosList("Global");



        try {
            importChaosLists();
        } catch (FileNotFoundException e) {
            Toast.makeText(MainActivity.this,   		"FileNotFoundException: " + e.getMessage(),                     Toast.LENGTH_SHORT).show();
        } catch (IOException e) {
            Toast.makeText(MainActivity.this,   		"IOException: " + e.getMessage(),                     Toast.LENGTH_SHORT).show();
        } catch (Exception e)
        {
            Toast.makeText(MainActivity.this,   		"Exception: " + e.getMessage(),                     Toast.LENGTH_SHORT).show();
        }
        
        addListenersOnButtons();

        if (savedInstanceState != null) {
            chaosText.setText(savedInstanceState.getCharSequence(STATE_CHAOS));
            globalText.setText(savedInstanceState.getCharSequence(STATE_GLOBAL));
        }

    }




    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putCharSequence(STATE_CHAOS, chaosText.getText());
        outState.putCharSequence(STATE_GLOBAL, globalText.getText());
    }

    public void importChaosLists() throws Exception {
        XmlPullParserFactory factory = XmlPullParserFactory.newInstance();
        factory.setNamespaceAware(false);
        XmlPullParser xpp = factory.newPullParser();

        xpp.setInput(this.getAssets().open("Chaos Magic.xml"), null);

        int eventType = xpp.getEventType();

        while (eventType != XmlPullParser.END_DOCUMENT) {

            if (eventType == XmlPullParser.START_TAG && xpp.getName().equals("chaoslist")) {

                eventType = xpp.next();
                while(eventType != XmlPullParser.END_TAG) {

                    if (eventType == XmlPullParser.START_TAG) {
                        String tagType = xpp.getName();
                        if (!tagType.equals("roll")) {
                            chaosText.append(xpp.getName());
                            throw new IOException("Expected tag <roll>");
                        }

                        eventType = xpp.next();
                        while (eventType != XmlPullParser.START_TAG) {
                            if (eventType == XmlPullParser.END_DOCUMENT) {
                                throw new IOException("No <list> tag found.");
                            }
                            eventType = xpp.next();
                        }

                        if (!xpp.getName().equals("list")) {
                            throw new IOException("Expected <list> tag.");
                        }

                        xpp.next();

                        String listName = xpp.getText();

                        if (!listName.equals("Global Chaos") && !listNames.contains(listName))
                        {
                            listNames.add(listName);
                            lists.add(new ChaosList(listName));
                        }

                        eventType = xpp.next();
                        while (eventType != XmlPullParser.END_TAG) {
                            if (eventType == XmlPullParser.END_DOCUMENT) {
                                throw new IOException("No </list> tag found.");
                            }
                            eventType = xpp.next();
                        }

                        if (!xpp.getName().equals("list")) {
                            throw new IOException("Expected </list> tag.");
                        }

                        eventType = xpp.next();
                        while (eventType != XmlPullParser.START_TAG) {
                            if (eventType == XmlPullParser.END_DOCUMENT) {
                                throw new IOException("No <name> tag found.");
                            }
                            eventType = xpp.next();
                        }

                        if (!xpp.getName().equals("name")) {
                            throw new IOException("Expected <name> tag.");
                        }

                        String rollName;

                        eventType = xpp.next();
                        if (eventType == XmlPullParser.END_TAG) {
                            rollName = "";
                        } else {
                            rollName = xpp.getText();
                            eventType = xpp.next();
                        }

                        while (eventType != XmlPullParser.END_TAG) {
                            if (eventType == XmlPullParser.END_DOCUMENT) {
                                throw new IOException("No </name> tag found.");
                            }
                            eventType = xpp.next();
                        }

                        if (!xpp.getName().equals("name")) {
                            throw new IOException("Expected </name> tag.");
                        }

                        eventType = xpp.next();
                        while (eventType != XmlPullParser.START_TAG) {
                            if (eventType == XmlPullParser.END_DOCUMENT) {
                                throw new IOException("No <effect> tag found.");
                            }
                            eventType = xpp.next();
                        }

                        if (!xpp.getName().equals("effect")) {
                            throw new IOException("Expected <effect> tag.");
                        }

                        String rollEffect;

                        eventType = xpp.next();
                        if (eventType == XmlPullParser.END_TAG) {
                            rollEffect = "";
                        } else {
                            rollEffect = xpp.getText();
                            eventType = xpp.next();
                        }

                        while (eventType != XmlPullParser.END_TAG) {
                            if (eventType == XmlPullParser.END_DOCUMENT) {
                                throw new IOException("No </effect> tag found.");
                            }
                            eventType = xpp.next();
                        }

                        if (!xpp.getName().equals("effect")) {
                            throw new IOException("Expected </effect> tag.");
                        }

                        while (eventType != XmlPullParser.START_TAG) {
                            if (eventType == XmlPullParser.END_DOCUMENT) {
                                throw new IOException("No <weight> tag found.");
                            }
                            eventType = xpp.next();
                        }

                        if (!xpp.getName().equals("weight")) {
                            throw new IOException("Expected <weight> tag.");
                        }

                        int weight;

                        eventType = xpp.next();
                        weight = Integer.parseInt(xpp.getText());
                        eventType = xpp.next();

                        while (eventType != XmlPullParser.END_TAG) {
                            if (eventType == XmlPullParser.END_DOCUMENT) {
                                throw new IOException("No </weight> tag found.");
                            }
                            eventType = xpp.next();
                        }

                        if (!xpp.getName().equals("weight")) {
                            throw new IOException("Expected </weight> tag.");
                        }

                        eventType = xpp.next();
                        while (eventType != XmlPullParser.END_TAG) {
                            if (eventType == XmlPullParser.END_DOCUMENT) {
                                throw new IOException("No </roll> tag found.");
                            }
                            eventType = xpp.next();
                        }

                        if (!xpp.getName().equals("roll")) {
                            throw new IOException("Expected </roll> tag.");
                        }

                        if (!listName.equals("Global Chaos")) {
                            lists.get(listNames.indexOf(listName)).addRoll(rollName, rollEffect, weight);
                        } else {
                            global.addRoll(rollName, rollEffect, weight);
                        }

                    }

                    if (eventType == XmlPullParser.END_DOCUMENT) {
                        throw new IOException("No closing </chaoslist> tag found.");
                    }

                    eventType = xpp.next();
                }

                if (!xpp.getName().equals("chaoslist")) {
                    throw new IOException("Expected closing </chaoslist> tag.");
                }
            }

            eventType = xpp.next();
        }
    }

    // get the selected dropdown list value
    public void addListenersOnButtons() {

        ArrayAdapter<String> listNameAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, listNames)
        {
            public View getView(int position, View convertView, android.view.ViewGroup parent) {
                TextView v = (TextView) super.getView(position, convertView, parent);
                v.setTypeface(customFont);
                return v;
            }

            public View getDropDownView(int position, View convertView, android.view.ViewGroup parent) {
                TextView v = (TextView) super.getView(position, convertView, parent);
                v.setTypeface(customFont);
                return v;
            }
        };

        listNameAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        chaosSpinner.setAdapter(listNameAdapter);


        globalButton.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                ChaosRoll roll = global.getRandom();
                globalText.setText(roll.rollName);
                globalText.append("\n\n" + roll.rollEffect);
            }
        });

        chaosButton.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {

                int listIndex = listNames.indexOf(chaosSpinner.getSelectedItem());
                ChaosRoll roll = lists.get(listIndex).getRandom();
                chaosText.setText(roll.rollName);
                //chaosText.setTypeface(null, Typeface.NORMAL);
                chaosText.append("\n\n" + roll.rollEffect);
                //Toast.makeText(MainActivity.this,    		"You chose " +                    String.valueOf(chaosSpinner.getSelectedItem()),                    Toast.LENGTH_SHORT).show();
            }

        });
    }

    public <ViewGroup> void customSpinner(){


    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return super.onCreateOptionsMenu(menu);
    }


}
