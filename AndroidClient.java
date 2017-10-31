import java.io.*;
import java.net.*;
import java.util.Date;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import javax.crypto.*;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import javax.crypto.spec.SecretKeySpec;
import javax.crypto.spec.IvParameterSpec;
import java.security.SecureRandom;

public class AndroidClient {
    public static void main(String argv[]) throws Exception {

        Socket clientSocket = new Socket("localhost", 65535);
        DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
        BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

        DateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
        String date = dateFormat.format(new Date());
        System.out.println(date);
        KeyGenerator KeyGen = null;

        try {
            KeyGen = KeyGenerator.getInstance("AES");
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        KeyGen.init(128);

        SecretKey SecKey = KeyGen.generateKey();

        //String encodedKey = Base64.getEncoder().encodeToString(SecKey.getEncoded());
        // decode the base64 encoded string
        //byte[] decodedKey = Base64.getDecoder().decode(encodedKey);
        // rebuild key using SecretKeySpec
        //SecretKey originalKey = new SecretKeySpec(decodedKey, 0, decodedKey.length, "AES");

        // build the initialization vector (randomly).
        //SecureRandom random = new SecureRandom();
        //generate random 16 byte IV AES is always 16 bytes
        // byte iv[] = new byte[16];
        //random.nextBytes(iv);

        // hardcode IV
        String IV = "This is a test!!";
        byte iv[] = IV.getBytes();

        IvParameterSpec ivspec = new IvParameterSpec(iv);


        Cipher AesCipher = null;

        try {
            String plaintext = date;

            AesCipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
            AesCipher.init(Cipher.ENCRYPT_MODE, SecKey, ivspec);

            String cipherText = Base64.getEncoder().encodeToString(AesCipher.doFinal(plaintext.getBytes("UTF-8")));
            //System.out.println("The secret key is: " + SecKey);
            System.out.println("The ciphertext is: " + cipherText);

            AesCipher.init(Cipher.DECRYPT_MODE, SecKey, ivspec);
            String decryptedText = new String(AesCipher.doFinal(Base64.getDecoder().decode(cipherText)));
            System.out.println("The plaintext is: " + decryptedText);

            String receive;
            try {
                outToServer.writeUTF(decryptedText + '\n');
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
    }
}
