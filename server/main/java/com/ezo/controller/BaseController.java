package com.ezo.controller;

import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;



@RestController
public class BaseController {
	
	
	@PostMapping("/api/test")
	public Map<String, Object> test(@RequestBody Map<String, Object> body) {
		System.out.println(body.toString());
		return body;
	}
	
	@RequestMapping("/api/test")
	public String test(@RequestParam(value= "code", required = false)String code, @RequestParam(value= "func", required = false)String func) {
		System.out.println("get");
		Stock stock = new Stock("ddd",555);
		return stock.exePy(code, func);
	}
	
	@RequestMapping("/api/sentiment")
	public String test(@RequestParam(value= "code", required = false)String code) {
		System.out.println("get");
		Stock stock = new Stock("ddd",555);
		return stock.exePySent(code);
	}
	
	@RequestMapping("/api/news")
	public String news(@RequestParam(value= "code", required = false)String code) {
		System.out.println("get");
		Stock stock = new Stock("ddd",555);
		return stock.exePyNews(code);
	}
	
	@RequestMapping("/api/exchange")
	public String exchange() {
		System.out.println("get");
		Stock stock = new Stock("ddd",555);
		return stock.exeExchange();
	}
}
