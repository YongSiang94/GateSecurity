package com.example.ksundararajan.cs3235;

import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.TextView;
import android.widget.ToggleButton;

import java.io.*;
import java.net.*;
import java.security.SecureRandom;
import java.util.Base64;

import java.security.Key;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.spec.AlgorithmParameterSpec;
import java.security.InvalidAlgorithmParameterException;
import java.util.Random;

import javax.crypto.*;
import javax.crypto.spec.SecretKeySpec;
import javax.crypto.spec.IvParameterSpec;

public class SendMessage extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_send_message);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);



        ToggleButton toggle = (ToggleButton) findViewById(R.id.toggleButton);
        toggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    // The toggle is enabled
                    System.out.println("Sending command to open");
                    new ConnectToPi().execute("open");
                    TextView message = (TextView) findViewById(R.id.textView);
                    message.setText("Tap to close the gate");

                } else {
                    // The toggle is disabled
                    System.out.println("Sending command to close");
                    new ConnectToPi().execute("close");
                    TextView message = (TextView) findViewById(R.id.textView);
                    message.setText("Tap to open the gate");
                }
            }
        });
    }



    public void closeGate(View view) throws IOException, InvalidAlgorithmParameterException {
        new ConnectToPi().execute("close");
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_send_message, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}


class ConnectToPi extends AsyncTask<String, Void, Void> {
    private static final String ENCRYPTION_KEY = "areyouokareyouok";
    private static String ENCRYPTION_IV = "0000000000000000";

    @Override
    protected Void doInBackground(String... params) {
        Socket clientSocket = null;
        try {
            clientSocket = new Socket("172.25.102.47", 65525);
            DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
            BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

            char[] CHARSET_AZ_09 = "0123456789".toCharArray();
            ENCRYPTION_IV = randomString(CHARSET_AZ_09, 16);

            try {
                outToServer.writeUTF(ENCRYPTION_IV);
                outToServer.flush();
            } catch (Exception e) {
                System.out.println(e);
            }

            Cipher AesCipher = null;

            try {
                String plaintext = params[0];

                AesCipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
                try {
                    AesCipher.init(Cipher.ENCRYPT_MODE, makeKey(), makeIv());
                } catch (InvalidAlgorithmParameterException e) {
                    e.printStackTrace();
                }

                String cipherText = null;
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                    cipherText = Base64.getEncoder().encodeToString(AesCipher.doFinal(plaintext.getBytes("UTF-8")));
                }
                System.out.println("The ciphertext is: " + cipherText);

                try {
                    AesCipher.init(Cipher.DECRYPT_MODE, makeKey(), makeIv());
                } catch (InvalidAlgorithmParameterException e) {
                    e.printStackTrace();
                }
                String decryptedText = null;
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                    decryptedText = new String(AesCipher.doFinal(Base64.getDecoder().decode(cipherText)));
                }
                System.out.println("The plaintext is: " + decryptedText);

                String receive;
                try {
                    outToServer.writeUTF(cipherText);
                    outToServer.flush();
                } catch (Exception e) {
                    System.out.println(e);
                }

                receive = inFromServer.readLine();
                System.out.println(receive);
                clientSocket.close();

            } catch (NoSuchAlgorithmException e) {
                e.printStackTrace();
            } catch (NoSuchPaddingException e) {
                e.printStackTrace();
            } catch (BadPaddingException e) {
                e.printStackTrace();
            } catch (IllegalBlockSizeException e) {
                e.printStackTrace();
            } catch (InvalidKeyException e) {
                e.printStackTrace();
            }

        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }

    static Key makeKey() {
        try {
            byte[] key = ENCRYPTION_KEY.getBytes("UTF-8");
            return new SecretKeySpec(key, "AES");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }

        return null;
    }

    static AlgorithmParameterSpec makeIv() {
        try {
            return new IvParameterSpec(ENCRYPTION_IV.getBytes("UTF-8"));
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return null;
    }

    static String randomString(char[] characterSet, int length) {
        Random random = new SecureRandom();
        char[] result = new char[length];
        for (int i = 0; i < result.length; i++) {
            // picks a random index out of character set > random character
            int randomCharIndex = random.nextInt(characterSet.length);
            result[i] = characterSet[randomCharIndex];
        }
        return new String(result);
    }
}
