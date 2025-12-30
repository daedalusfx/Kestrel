const { getHistoricalRates } = require('dukascopy-node');
const { format, addMonths, startOfMonth, endOfMonth, isBefore } = require('date-fns');
const fs = require('fs').promises;
const path = require('path');

// --- تنظیمات ---
const config = {
    instruments: ['eurjpy', 'gbpjpy', 'gbpaud'],
    timeframes: ['m5', 'm15', 'h1', 'd1'],
    startDate: new Date('2023-01-01'),
    endDate: new Date('2023-12-31'),
    outputDir: './data_merged'
};

async function downloadAndMerge() {
    await fs.mkdir(config.outputDir, { recursive: true });

    for (const instrument of config.instruments) {
        for (const tf of config.timeframes) {
            let allData = [];
            let currentMonthStart = startOfMonth(config.startDate);

            console.log(`🚀 Processing ${instrument.toUpperCase()} - ${tf}...`);

            while (isBefore(currentMonthStart, config.endDate)) {
                const fromDate = currentMonthStart;
                const toDate = endOfMonth(currentMonthStart);
                
                console.log(`   ⏳ Fetching: ${format(fromDate, 'yyyy-MM')}`);

                try {
                    // ساختار جدید طبق داکیومنت ارسالی شما
                    const data = await getHistoricalRates({
                        instrument: instrument,
                        dates: {
                            from: fromDate,
                            to: toDate
                        },
                        timeframe: tf, // تغییر از interval به timeframe
                        format: 'json',
                        volumes: true,
                        ignoreFlats: true, // حذف روزهای تعطیل
                        useCache: true,    // استفاده از کش برای سرعت بیشتر
                        retryCount: 2      // تلاش مجدد در صورت خطا
                    });

                    if (data && data.length > 0) {
                        allData = allData.concat(data);
                    }
                } catch (error) {
                    // نمایش جزئیات خطا برای دیباگ بهتر
                    console.error(`   ❌ Error in ${format(fromDate, 'yyyy-MM')}:`, error.message || error);
                }

                currentMonthStart = addMonths(currentMonthStart, 1);
            }

            // --- ذخیره فایل نهایی ---
            if (allData.length > 0) {
                allData.sort((a, b) => a.timestamp - b.timestamp);
                
                const fileName = `${instrument.toUpperCase()}-${tf}.json`;
                const filePath = path.join(config.outputDir, fileName);
                
                await fs.writeFile(filePath, JSON.stringify(allData, null, 2));
                console.log(`   ✅ Success: ${fileName} saved. Total candles: ${allData.length}`);
            }
        }
    }
}

downloadAndMerge().catch(console.error);