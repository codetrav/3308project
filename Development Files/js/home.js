	var speed = ;
	var engine = ;
	var rpm = ;
	var maf = ;
	var fuelRate = ;
	var battery = ;
	var ambientTemp = ;
	var intakeTemp = ;
	var coolantTemp = ;
	var o2Sensor1 = ;
	var o2Sensor2 = ;
	var heatSensor1 = ;
	var heatSensor2 = ;




	document.getElementById("speedText").innerHTML = "Speed: " speed;
	document.getElementById("engineText").innerHTML = "Engine Temp: " engine; 
	document.getElementById("rpmText").innerHTML = "RPM: " rpm;
	document.getElementById("mafText").innerHTML = "MAF: " maf;
	document.getElementById("fuelRateText").innerHTML = "Fuel Rate: " fuelRate;
	document.getElementById("batteryText").innerHTML = "Battery: " battery;

	//change spedometer image
	//low
	if( speed < )
	{
		document.getElementById("speedImage").src = "widgets/spedometer/low.svg";
	}
	//medium
	if( < speed < )
	{
		document.getElementById("speedImage").src = "widgets/spedometer/medium.svg";
	}
	//high
	if(speed > )
	{
		document.getElementById("speedImage").src = "widgets/spedometer/high.svg";
	}

	//change engine temp image 
	//low 
	if( engine < )
	{
		document.getElementById("engineImage").src = "widgets/thermometer/low.svg";
	}
	//medium
	if( < engine < )
	{
		document.getElementById("engineImage").src = "widgets/thermometer/medium.svg";
	}
	//high 
	if(engine > )
	{
		document.getElementById("engineImage").src = "widgets/thermometer/high.svg";
	}

	//change rpm image 
	//low
	if( rpm < )
	{
		document.getElementById("rpmImage").src = "widgets/rpm/low.svg";
	}
	//medium 
	if( < rpm < )
	{
		document.getElementById("rpmImage").src = "widgets/rpm/medium.svg";
	}
	//high 
	if( rpm > )
	{
		document.getElementById("rpmImage").src = "widgets/rpm/high.svg";
	}

	//change MAF image 
	//low 
	if( maf < )
	{
		document.getElementById("mafImage").src = "widgets/maf/low.svg";
	}
	//medium 
	if( < maf < )
	{
		document.getElementById("mafImage").src = "widgets/maf/medium.svg";
	}

	//high 
	if( maf > )
	{
		document.getElementById("mafImage").src = "widgets/maf/high.svg";
	}

	//change fuel rate image 
	//low
	if(fuelRate < )
	{
		document.getElementById("fuelImage").src = "widgets/fuel-rate/low.svg";
	}
	//medium
	if( < fuelRate < )
	{
		document.getElementById("fuelImage").src = "widgets/fuel-rate/medium.svg";
	}
	//high 
	if( fuelRate > )
	{
		document.getElementById("fuelImage").src = "widgets/fuel-rate/high.svg";
	}

	//change battery image 
	//low 
	if(battery < )
	{
		document.getElementById("batteryImage").src = "widgets/battery/low.svg";
	}
	//medium 
	if( < battery < )
	{
		document.getElementById("batteryImage").src = "widgets/battery/medium.svg";
	}
	//high 
	if(battery > )
	{
		document.getElementById("batteryImage").src = "widgets/battery/high.svg";
	}

	//change ambient temp image
	//low 
	if(ambientTemp < )
	{
		document.getElementById("guageImage1").src = "widgets/guages/low.svg";
	}
	//good temp
	if( < ambientTemp < )
	{
		document.getElementById("guageImage1").src = "widgets/guages/good.svg";
	}
	//high
	if(ambientTemp > )
	{
	document.getElementById("guageImage1").src = "widgets/guages/high.svg";
	}

	//change intake temp image
	//low
	if(intakeTemp < )
	{
		document.getElementById("guageImage2").src = "widgets/guages/low.svg";
	}
	//good temp 
	if( < intakeTemp < )
	{
		document.getElementById("guageImage2").src = "widgets/guages/good.svg";
	}
	//high
	if(intakeTemp > )
	{
		document.getElementById("guageImage2").src = "widgets/guages/high.svg";
	}

	//chance coolant temp image 
	//low 
	if(coolantTemp < )
	{
		document.getElementById("guageImage3").src = "widgets/guages/low.svg";
	}
	//good temp
	if( < coolantTemp < )
	{
		document.getElementById("guageImage3").src = "widgets/guages/good.svg";
	}
	//high
	if( coolantTemp > )
	{
		document.getElementById("guageImage3").src = "widgets/guages/high.svg";
	}

	//o2 sensor 1 
	//low
	if(o2Sensor1 == 0)
	{
		document.getElementById("o2Image1").src = "widgets/guages/bad.svg";
	}
	//high
	if(o2Sensor1 == 1)
	{
		document.getElementById("o2Image1").src = "widgets/guages/good.svg";
	}

	//o2 sensor 2 
	//low 
	if( o2Sensor2 == 0)
	{
		document.getElementById("o2Image2").src = "widgets/guages/bad.svg";
	}
	//high 
	if(o2Sensor2 ==1)
	{
		document.getElementById("o2Image2").src = "widgets/guages/good.svg";
	}


	var commandErrors = [40];

	if (commandErrors >= 70) {
		document.getElementById("centerbox1").style.color = 'red';
	  }
	else
	if (commandErrors >= 51 && udata <70)  
	  {
	  document.getElementById("centerbox1").style.color = 'yellow';
	  }
	  else
	  if (commandErrors <=50)
	  {
	  document.getElementById("centerbox1").style.color = 'green';
	  }
