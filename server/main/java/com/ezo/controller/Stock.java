package com.ezo.controller;

import lombok.Getter;
import lombok.Setter;
import lombok.AllArgsConstructor;

import org.apache.commons.exec.CommandLine;
import org.apache.commons.exec.DefaultExecutor;
import org.apache.commons.exec.PumpStreamHandler;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
@Setter
@Getter
@AllArgsConstructor
public class Stock {
	
	private String code;
	int price;
	
	public String exePy(String code, String func) {
		String output = "null";
		
		System.out.println("Python Call");
        String[] command = new String[4];
        command[0] = "python";
        command[1] = "E:/최종프로젝트/news_crawler/print.py";
        if (code == null)
        	command[2] = "5930";
        else
        	command[2] = code;
        
        if ( func != null )
        	command[3] = func;
        
        
        CommandLine commandLine = CommandLine.parse(command[0]);
        for (int i = 1, n = command.length; i < n; i++) {
            commandLine.addArgument(command[i]);
        }
        
        System.out.println(commandLine);
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PumpStreamHandler pumpStreamHandler = new PumpStreamHandler(outputStream);
        DefaultExecutor executor = new DefaultExecutor();
        executor.setStreamHandler(pumpStreamHandler);
        try {
        	 int result = executor.execute(commandLine);
             //System.out.println("result: " + result);
             output = new String(outputStream.toByteArray(), "MS949");
        } catch (Exception e) {
        	e.printStackTrace();
        }
        
        
        //System.out.print(output);
        return output;
        
       
	}
	
	public String exePySent(String code) {
		String output = "null";
		
		System.out.println("Python Call");
        String[] command = new String[4];
        command[0] = "python";
        command[1] = "E:/최종프로젝트/news_crawler/print_sentiment.py";
        if (code == null)
        	command[2] = "5930";
        else
        	command[2] = code;
        
        
        CommandLine commandLine = CommandLine.parse(command[0]);
        for (int i = 1, n = command.length; i < n; i++) {
            commandLine.addArgument(command[i]);
        }
        
        System.out.println(commandLine);
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PumpStreamHandler pumpStreamHandler = new PumpStreamHandler(outputStream);
        DefaultExecutor executor = new DefaultExecutor();
        executor.setStreamHandler(pumpStreamHandler);
        try {
        	 int result = executor.execute(commandLine);
             //System.out.println("result: " + result);
             output = new String(outputStream.toByteArray(), "MS949");
        } catch (Exception e) {
        	e.printStackTrace();
        }
        
        
        //System.out.print(output);
        return output;
        
       
	}
	
	public String exePyNews(String code) {
		String output = "null";
		
		System.out.println("API Call : api/news " + code);
        String[] command = new String[4];
        command[0] = "python";
        command[1] = "E:/최종프로젝트/news_crawler/print_news.py";
        if (code == null)
        	command[2] = "5930";
        else
        	command[2] = code;
        
        
        CommandLine commandLine = CommandLine.parse(command[0]);
        for (int i = 1, n = command.length; i < n; i++) {
            commandLine.addArgument(command[i]);
        }
        
        System.out.println(commandLine);
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PumpStreamHandler pumpStreamHandler = new PumpStreamHandler(outputStream);
        DefaultExecutor executor = new DefaultExecutor();
        executor.setStreamHandler(pumpStreamHandler);
        try {
        	 int result = executor.execute(commandLine);
             //System.out.println("result: " + result);
             output = new String(outputStream.toByteArray(), "MS949");
        } catch (Exception e) {
        	e.printStackTrace();
        }
        
        
        //System.out.print(output);
        return output;
        
       
	}
	
	public String probuildNews(String code) {
		String command = "python";  // 명령어
		String arg1 = "E:/최종프로젝트/news_crawler/print_news.py"; // 인자
		String arg2 = code;
		ProcessBuilder builder = new ProcessBuilder(command, arg1,arg2);
		try {
			Process process = builder.start();
			int exitVal = process.waitFor();  // 자식 프로세스가 종료될 때까지 기다림

			BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream(), "euc-kr")); //
			String line;
			while ((line = br.readLine()) != null) {
			     System.out.println(">>>  " + line); // 표준출력에 쓴다
			}
			if(exitVal != 0) {
			  // 비정상 종료
			  System.out.println("서브 프로세스가 비정상 종료되었다.");
			}
		}
		catch (Exception e)
		{
			System.out.println(e); // 
		}
		return "1";
	}
	
	public String exeExchange() {
		String output = "null";
		
		System.out.println("API Call : api/exchange ");
        String[] command = new String[4];
        command[0] = "python";
        command[1] = "E:/최종프로젝트/news_crawler/print_exchange.py";
       
        
        CommandLine commandLine = CommandLine.parse(command[0]);
        for (int i = 1, n = command.length; i < n; i++) {
            commandLine.addArgument(command[i]);
        }
        
        System.out.println(commandLine);
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PumpStreamHandler pumpStreamHandler = new PumpStreamHandler(outputStream);
        DefaultExecutor executor = new DefaultExecutor();
        executor.setStreamHandler(pumpStreamHandler);
        try {
        	 int result = executor.execute(commandLine);
             //System.out.println("result: " + result);
             output = new String(outputStream.toByteArray(), "MS949");
        } catch (Exception e) {
        	e.printStackTrace();
        }
        
        
        //System.out.print(output);
        return output;
        
       
	}
}
